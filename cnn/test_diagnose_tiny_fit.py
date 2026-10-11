"""Synthetic trace parity and ambiguous one-to-one matching regression."""
import numpy as np

from .diagnose_tiny_fit import assign, reason_for, support, trace_heads
from .integer import _decode


def main():
    heads = [np.zeros((288 // stride, 512 // stride, 7), dtype=np.int16) for stride in (4, 8, 16)]
    for head in heads:
        head[..., 4:] = -4096
    # Two equally scored, identical boxes: lower cell wins and suppresses cell1.
    heads[0][0, 0, :2] = 512
    heads[0][0, 1, :2] = [256, 512]
    heads[0][0, :2, 4:6] = 1024
    boxes, _, traces = trace_heads(heads)
    assert traces[0]["final"][0]["cell_id"] == 0
    assert traces[0]["removed"][1] == dict(stage="NMS", suppressor_cell=0)
    assert boxes[0].tolist() == [v / 256 for v in _decode(heads[0][0, 0, :4], 0, 0, 4)]
    for cell in (0, 127, 9215, 9216, 12095):
        if cell < 9216:
            index, stride, local = 0, 4, cell
        elif cell < 11520:
            index, stride, local = 1, 8, cell - 9216
        else:
            index, stride, local = 2, 16, cell - 11520
        y, x = divmod(local, 512 // stride)
        assert boxes[cell].tolist() == [v / 256 for v in _decode(heads[index][y, x, :4], x, y, stride)]
    # Sparse non-overlapping boxes test Top128 and output cap separately.
    for head in heads:
        head[..., 4:] = -4096
        head[..., :4] = 0
    heads[0][2:5, 2:50, 4:6] = 1024
    _, _, traces = trace_heads(heads)
    assert traces[0]["above_floor_count"] == 144
    assert len(traces[0]["top"]) == 128 and len(traces[0]["final"]) == 32
    assert any(row["stage"] == "output_cap32" for row in traces[0]["removed"].values())
    gt = [dict(box=[0, 0, 10, 10]), dict(box=[1, 0, 11, 10])]
    pred = [dict(box=[0, 0, 10, 10], score=.9, cell_id=0)]
    assert assign(pred, gt, .05) == {0: 0}
    stages = {"final": support(pred, gt[1])}
    assert reason_for(stages, {}) == "shared_candidate"
    assert support([], gt[0])["best_IoU"] == 0
    print("PASS stage parity, NMS ties, Top128, output32, grid boundaries and shared-GT matching")


if __name__ == "__main__":
    main()
