"""Small CPU checks for native review conversion and supervised ignore behavior."""
import copy
import numpy as np
import torch
from .prepare_verified_train import convert_frame, duplicate_hints
from .loss import YOLOXLoss


def main():
    torch.set_num_threads(2)
    image = dict(bucket="train_review", split="train", manual_review=dict(complete=True),
                 width=1000, height=1000, image_id="test", legacy_id="test", raw_file_absolute="unused",
                 source_sha256="a"*64, source_scene_id="fixture", camera_id="fixture",
                 frame_index=1, source_metadata=dict(frame_base=1), labels=[
                     dict(target_id="o1", **{"class":"person"}, bbox=[100,100,200,200]),
                     dict(target_id="i1", **{"class":"ignore"}, bbox=[0,0,1000,1000])])
    row = convert_frame(image)
    np.testing.assert_allclose(row["boxes"], [[140.8,28.8,169.6,57.6]], atol=1e-6)
    assert row["source_frame"] == 0 and row["labels"] == [0] and len(row["ignore_boxes"]) == 1
    for field, value in (("split", "val"), ("manual_review", dict(complete=False))):
        bad = copy.deepcopy(image); bad[field] = value
        try:
            convert_frame(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("unsafe review accepted")
    bad = copy.deepcopy(image); bad["labels"][0]["bbox"][0] = float("nan")
    try:
        convert_frame(bad)
    except ValueError:
        pass
    else:
        raise AssertionError("NaN accepted")
    duplicate = copy.deepcopy(image["labels"][0]); duplicate["target_id"] = "o2"
    image["labels"].append(duplicate)
    assert len(duplicate_hints(image)) == 1 and len(image["labels"]) == 3
    outputs = [torch.zeros((1,7,size,size), requires_grad=True) for size in (4,2,1)]
    result = YOLOXLoss()(outputs, [dict(boxes=torch.tensor([[0.,0.,4.,4.]]),
                                      labels=torch.tensor([0]),
                                      ignore_boxes=torch.tensor([[0.,0.,512.,288.]]))])
    assert result["num_foreground"] > 0 and torch.isfinite(result["loss"])
    result["loss"].backward()
    object_gradients = torch.cat([output.grad[:,4].reshape(-1) for output in outputs])
    assert (object_gradients < 0).any() and not (object_gradients > 0).any()
    print("PASS: native/letterbox coordinates, frame base, rejection, duplicate hints, positive supervision inside ignore")


if __name__ == "__main__":
    main()
