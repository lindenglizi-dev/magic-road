"""YOLOX-style decoding, SimOTA assignment, and training losses."""

from __future__ import annotations

from typing import Sequence

import torch
from torch import Tensor, nn
import torch.nn.functional as F

try:
    from .model import NUM_CLASSES, STRIDES
except ImportError:  # direct execution/import from cnn/
    from model import NUM_CLASSES, STRIDES


TW_TH_MIN = -4.0
TW_TH_MAX = 3.5


def pairwise_iou(boxes1: Tensor, boxes2: Tensor) -> Tensor:
    """Pairwise IoU for xyxy boxes."""
    top_left = torch.maximum(boxes1[:, None, :2], boxes2[None, :, :2])
    bottom_right = torch.minimum(boxes1[:, None, 2:], boxes2[None, :, 2:])
    intersection = (bottom_right - top_left).clamp_min(0).prod(dim=2)
    area1 = (boxes1[:, 2:] - boxes1[:, :2]).clamp_min(0).prod(dim=1)
    area2 = (boxes2[:, 2:] - boxes2[:, :2]).clamp_min(0).prod(dim=1)
    return intersection / (area1[:, None] + area2[None, :] - intersection).clamp_min(1e-8)


def aligned_iou(boxes1: Tensor, boxes2: Tensor) -> Tensor:
    top_left = torch.maximum(boxes1[:, :2], boxes2[:, :2])
    bottom_right = torch.minimum(boxes1[:, 2:], boxes2[:, 2:])
    intersection = (bottom_right - top_left).clamp_min(0).prod(dim=1)
    area1 = (boxes1[:, 2:] - boxes1[:, :2]).clamp_min(0).prod(dim=1)
    area2 = (boxes2[:, 2:] - boxes2[:, :2]).clamp_min(0).prod(dim=1)
    return intersection / (area1 + area2 - intersection).clamp_min(1e-8)


def decode_outputs(outputs: Sequence[Tensor]) -> tuple[Tensor, Tensor, Tensor, Tensor, Tensor]:
    """Decode three raw heads into boxes, logits, centers, and per-anchor strides."""
    if len(outputs) != len(STRIDES):
        raise ValueError(f"expected {len(STRIDES)} output scales, got {len(outputs)}")
    boxes, objectness, classes, centers, anchor_strides = [], [], [], [], []
    for output, stride in zip(outputs, STRIDES):
        if output.ndim != 4 or output.shape[1] != 5 + NUM_CLASSES:
            raise ValueError("each output must have shape [B, 7, H, W]")
        batch, _channels, height, width = output.shape
        raw = output.permute(0, 2, 3, 1).reshape(batch, -1, 5 + NUM_CLASSES)
        y, x = torch.meshgrid(
            torch.arange(height, device=output.device, dtype=output.dtype),
            torch.arange(width, device=output.device, dtype=output.dtype), indexing="ij")
        grid = torch.stack((x, y), dim=-1).reshape(1, -1, 2)
        center = (grid + 0.5) * stride
        xy = (raw[..., :2] + grid) * stride
        # This is the same finite range implemented by integer.exponent.
        wh = raw[..., 2:4].clamp(TW_TH_MIN, TW_TH_MAX).exp() * stride
        boxes.append(torch.cat((xy - wh / 2, xy + wh / 2), dim=-1))
        objectness.append(raw[..., 4])
        classes.append(raw[..., 5:])
        centers.append(center.expand(batch, -1, -1))
        anchor_strides.append(torch.full((batch, height * width), stride,
                                         device=output.device, dtype=output.dtype))
    return (torch.cat(boxes, dim=1), torch.cat(objectness, dim=1),
            torch.cat(classes, dim=1), torch.cat(centers, dim=1),
            torch.cat(anchor_strides, dim=1))


def _candidate_mask(gt_boxes: Tensor, centers: Tensor, strides: Tensor,
                    center_radius: float) -> tuple[Tensor, Tensor]:
    x, y = centers[:, 0], centers[:, 1]
    left = x[None] - gt_boxes[:, 0, None]
    top = y[None] - gt_boxes[:, 1, None]
    right = gt_boxes[:, 2, None] - x[None]
    bottom = gt_boxes[:, 3, None] - y[None]
    in_boxes = torch.stack((left, top, right, bottom), dim=-1).amin(dim=-1) > 0

    gt_centers = (gt_boxes[:, :2] + gt_boxes[:, 2:]) / 2
    radius = center_radius * strides[None]
    center_left = x[None] - (gt_centers[:, 0, None] - radius)
    center_top = y[None] - (gt_centers[:, 1, None] - radius)
    center_right = (gt_centers[:, 0, None] + radius) - x[None]
    center_bottom = (gt_centers[:, 1, None] + radius) - y[None]
    in_centers = torch.stack((center_left, center_top, center_right, center_bottom),
                             dim=-1).amin(dim=-1) > 0
    candidates = (in_boxes | in_centers).any(dim=0)
    if not candidates.any():
        candidates[:] = True
    return candidates, (in_boxes[:, candidates] & in_centers[:, candidates])


def _dynamic_k_matching(cost: Tensor, pair_ious: Tensor,
                        candidate_mask: Tensor) -> tuple[Tensor, Tensor, Tensor]:
    matching = torch.zeros_like(cost, dtype=torch.bool)
    topk = min(10, pair_ious.shape[1])
    dynamic_ks = pair_ious.topk(topk, dim=1).values.sum(dim=1).to(torch.int64).clamp_min(1)
    for gt_index, dynamic_k in enumerate(dynamic_ks.tolist()):
        selected = cost[gt_index].topk(dynamic_k, largest=False).indices
        matching[gt_index, selected] = True

    multiple = matching.sum(dim=0) > 1
    if multiple.any():
        best_gt = cost[:, multiple].argmin(dim=0)
        matching[:, multiple] = False
        matching[best_gt, multiple] = True

    candidate_foreground = matching.any(dim=0)
    foreground = candidate_mask.clone()
    foreground[candidate_mask] = candidate_foreground
    matched_gt = matching[:, candidate_foreground].to(torch.float32).argmax(dim=0)
    matched_iou = (matching[:, candidate_foreground] *
                   pair_ious[:, candidate_foreground]).sum(dim=0)
    return foreground, matched_gt, matched_iou


def simota_assign(pred_boxes: Tensor, object_logits: Tensor, class_logits: Tensor,
                  centers: Tensor, strides: Tensor, gt_boxes: Tensor, gt_labels: Tensor,
                  center_radius: float = 2.5) -> tuple[Tensor, Tensor, Tensor]:
    """Official YOLOX SimOTA structure: center prior, dynamic-k, conflict resolve."""
    # Matching is detached FP32 bookkeeping. BCE(probability) is intentionally
    # outside autocast; PyTorch rejects that operation in an autocast region.
    with torch.amp.autocast(device_type=pred_boxes.device.type, enabled=False):
        candidates, in_boxes_and_center = _candidate_mask(gt_boxes, centers, strides,
                                                           center_radius)
        candidate_boxes = pred_boxes[candidates].float()
        pair_ious = pairwise_iou(gt_boxes.float(), candidate_boxes)
        iou_cost = -torch.log(pair_ious.clamp_min(1e-8))

        gt_one_hot = F.one_hot(gt_labels, NUM_CLASSES).float()
        probabilities = torch.sqrt(
            class_logits[candidates].float().sigmoid()
            * object_logits[candidates].float().sigmoid()[:, None]
        ).clamp(1e-6, 1 - 1e-6)
        cls_cost = F.binary_cross_entropy(
            probabilities[None].expand(gt_boxes.shape[0], -1, -1),
            gt_one_hot[:, None].expand(-1, probabilities.shape[0], -1), reduction="none"
        ).sum(dim=2)
        cost = cls_cost + 3.0 * iou_cost + 100_000.0 * (~in_boxes_and_center)
        foreground, matched_gt, matched_iou = _dynamic_k_matching(cost, pair_ious, candidates)
    return foreground, matched_gt, matched_iou


def _ignore_anchor_mask(ignore_boxes: Tensor, pred_boxes: Tensor, centers: Tensor,
                        iou_threshold: float) -> Tensor:
    if ignore_boxes.numel() == 0:
        return torch.zeros(pred_boxes.shape[0], dtype=torch.bool, device=pred_boxes.device)
    inside = (
        (centers[:, 0][None] >= ignore_boxes[:, 0, None])
        & (centers[:, 0][None] <= ignore_boxes[:, 2, None])
        & (centers[:, 1][None] >= ignore_boxes[:, 1, None])
        & (centers[:, 1][None] <= ignore_boxes[:, 3, None])
    ).any(dim=0)
    overlaps = pairwise_iou(ignore_boxes, pred_boxes).amax(dim=0) >= iou_threshold
    return inside | overlaps


class YOLOXLoss(nn.Module):
    """IoU, objectness, and class losses normalized by SimOTA foreground count."""

    def __init__(self, iou_weight: float = 5.0, center_radius: float = 2.5,
                 ignore_iou: float = 0.5) -> None:
        super().__init__()
        self.iou_weight = iou_weight
        self.center_radius = center_radius
        self.ignore_iou = ignore_iou

    def forward(self, outputs: Sequence[Tensor], targets: Sequence[dict[str, Tensor]]
                ) -> dict[str, Tensor]:
        boxes, object_logits, class_logits, centers, strides = decode_outputs(outputs)
        if len(targets) != boxes.shape[0]:
            raise ValueError("target count must equal batch size")

        iou_sum = boxes.new_zeros(())
        object_sum = boxes.new_zeros(())
        class_sum = boxes.new_zeros(())
        total_foreground = 0
        total_gt = 0

        for index, target in enumerate(targets):
            gt_boxes = torch.as_tensor(target["boxes"], device=boxes.device,
                                       dtype=torch.float32).reshape(-1, 4)
            gt_labels = torch.as_tensor(target["labels"], device=boxes.device,
                                        dtype=torch.long).reshape(-1)
            ignore_boxes = torch.as_tensor(target.get("ignore_boxes", []), device=boxes.device,
                                           dtype=torch.float32).reshape(-1, 4)
            if gt_boxes.shape[0] != gt_labels.shape[0]:
                raise ValueError("boxes and labels must have equal length")
            if gt_labels.numel() and ((gt_labels < 0) | (gt_labels >= NUM_CLASSES)).any():
                raise ValueError("labels must be 0 (person) or 1 (vehicle)")

            with torch.no_grad():
                ignore = _ignore_anchor_mask(ignore_boxes, boxes[index].detach(),
                                             centers[index], self.ignore_iou)
                if gt_boxes.numel():
                    foreground, matched_gt, matched_iou = simota_assign(
                        boxes[index].detach().float(), object_logits[index].detach().float(),
                        class_logits[index].detach().float(), centers[index].float(),
                        strides[index].float(), gt_boxes, gt_labels, self.center_radius)
                else:
                    foreground = torch.zeros_like(object_logits[index], dtype=torch.bool)
                    matched_gt = torch.empty(0, dtype=torch.long, device=boxes.device)
                    matched_iou = boxes.new_empty(0)
                ignore[foreground] = False

            object_target = foreground.to(object_logits.dtype)
            object_loss = F.binary_cross_entropy_with_logits(
                object_logits[index], object_target, reduction="none")
            object_sum = object_sum + object_loss[~ignore].sum()

            foreground_count = int(foreground.sum().item())
            total_foreground += foreground_count
            total_gt += int(gt_boxes.shape[0])
            if foreground_count:
                matched_boxes = gt_boxes[matched_gt]
                iou = aligned_iou(boxes[index, foreground].float(), matched_boxes)
                iou_sum = iou_sum + (1.0 - iou.square()).sum()
                class_target = F.one_hot(gt_labels[matched_gt], NUM_CLASSES).to(
                    class_logits.dtype) * matched_iou[:, None].to(class_logits.dtype)
                class_sum = class_sum + F.binary_cross_entropy_with_logits(
                    class_logits[index, foreground], class_target, reduction="sum")

        normalizer = max(total_foreground, 1)
        iou_loss = iou_sum / normalizer
        object_loss = object_sum / normalizer
        class_loss = class_sum / normalizer
        total = self.iou_weight * iou_loss + object_loss + class_loss
        return {
            "loss": total,
            "iou_loss": iou_loss.detach(),
            "object_loss": object_loss.detach(),
            "class_loss": class_loss.detach(),
            "num_foreground": boxes.new_tensor(float(total_foreground)),
            "num_gt": boxes.new_tensor(float(total_gt)),
        }


DISTILL_CONTRACT = {
    "name": "gt_supported_foreground_distill_v2",
    "teacher_score_min": 0.3, "gt_iou_min": 0.5, "ignore_iou": 0.5,
    "background": "supervised_GT_loss_only",
    "foreground": "mapped_class_argmax_and_score_and_same_class_GT_support_required",
}


def dense_distillation_loss(student: Sequence[Tensor], teacher: Sequence[Tensor],
                            targets: Sequence[dict[str, Tensor]],
                            box_weight: float = 1.0, object_weight: float = 1.0,
                            class_weight: float = 1.0) -> Tensor:
    """Distill GT-supported foreground only; never supervise unknown/background regions.

    The COCO teacher's objectness covers 80 categories. Its box/objectness may
    teach this two-class student only when a mapped class has sufficient score
    and the decoded box matches an existing same-class GT. Ignore regions have
    zero distillation gradient, even when the teacher confidently predicts there.
    The unchanged supervised loss remains responsible for background learning.
    """
    if len(student) != len(teacher) or len(student) != len(STRIDES):
        raise ValueError("student and cached teacher must have the same output scales")
    for student_scale, teacher_scale in zip(student, teacher):
        if student_scale.shape != teacher_scale.shape:
            raise ValueError(f"teacher shape {teacher_scale.shape} != student {student_scale.shape}")
    teacher = [scale.detach().to(student[0].device, dtype=torch.float32) for scale in teacher]
    teacher_boxes, object_logits, class_logits, centers, _ = decode_outputs(teacher)
    if len(targets) != teacher_boxes.shape[0]:
        raise ValueError("distillation target count must equal batch size")
    raw_student = torch.cat([scale.permute(0, 2, 3, 1).reshape(scale.shape[0], -1, 7)
                             for scale in student], dim=1).float()
    raw_teacher = torch.cat([scale.permute(0, 2, 3, 1).reshape(scale.shape[0], -1, 7)
                             for scale in teacher], dim=1)
    importance = torch.zeros_like(object_logits)
    with torch.no_grad():
        scores = object_logits.sigmoid()[..., None] * class_logits.sigmoid()
        for index, target in enumerate(targets):
            gt = torch.as_tensor(target["boxes"], device=raw_student.device,
                                 dtype=torch.float32).reshape(-1, 4)
            labels = torch.as_tensor(target["labels"], device=raw_student.device,
                                     dtype=torch.long).reshape(-1)
            if (gt.shape[0] != labels.shape[0] or not torch.isfinite(gt).all()
                    or (gt[:, 2:] <= gt[:, :2]).any()
                    or ((labels < 0) | (labels >= NUM_CLASSES)).any()):
                raise ValueError("invalid distillation ground truth")
            if gt.numel():
                ious = pairwise_iou(gt, teacher_boxes[index])
                class_scores = scores[index][:, labels].T
                supported = ((ious >= DISTILL_CONTRACT["gt_iou_min"])
                             & (class_scores >= DISTILL_CONTRACT["teacher_score_min"])
                             & (class_logits[index].argmax(dim=-1)[None] == labels[:, None]))
                importance[index] = (class_scores * supported).amax(dim=0)
            ignores = torch.as_tensor(target.get("ignore_boxes", []),
                                      device=raw_student.device, dtype=torch.float32).reshape(-1, 4)
            if not torch.isfinite(ignores).all() or (ignores[:, 2:] <= ignores[:, :2]).any():
                raise ValueError("invalid distillation ignore region")
            mask = _ignore_anchor_mask(ignores, teacher_boxes[index], centers[index],
                                       DISTILL_CONTRACT["ignore_iou"])
            importance[index, mask] = 0
    foreground = importance > 0
    if not foreground.any():
        return raw_student.sum() * 0  # Connected zero: unsupported/ignored anchors cannot teach.
    prediction, target = raw_student[foreground], raw_teacher[foreground]
    weights = importance[foreground]
    box = F.smooth_l1_loss(prediction[:, :4], target[:, :4], reduction="none").sum(dim=1)
    obj = F.binary_cross_entropy_with_logits(prediction[:, 4], target[:, 4].sigmoid(),
                                             reduction="none")
    cls = F.binary_cross_entropy_with_logits(prediction[:, 5:], target[:, 5:].sigmoid(),
                                             reduction="none").sum(dim=1)
    return ((box_weight * box + object_weight * obj + class_weight * cls) * weights).sum() / weights.sum().clamp_min(1)


__all__ = [
    "DISTILL_CONTRACT", "TW_TH_MAX", "TW_TH_MIN", "YOLOXLoss", "aligned_iou", "decode_outputs",
    "dense_distillation_loss", "pairwise_iou", "simota_assign",
]
