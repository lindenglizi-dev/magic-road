"""CPU proof of audit-only decoder geometry against the training decoder."""
import numpy as np
import torch

from .build_verified_review import decode_heads, self_test
from .dataset import _letterbox_transform
from .loss import decode_outputs


def main():
    torch.set_num_threads(2)
    self_test()
    for width, height in ((1280,720), (1344,756), (1000,1000), (720,1280)):
        heads = [torch.full((1,7,288//stride,512//stride), -80.0)
                 for stride in (4,8,16)]
        heads[0][0,:4,36,64] = torch.tensor([.25,.5,.3,-.2])
        heads[0][0,4:6,36,64] = 0
        transform = _letterbox_transform(width,height)
        candidates = decode_heads(heads,transform)
        assert len(candidates) == 1
        candidate = candidates[0]
        boxes, objects, classes, _, _ = decode_outputs(heads)
        index = 36*128+64
        network = boxes[0,index].numpy()
        network = np.clip(network,0,[512,288,512,288])
        expected = [(network[i]*2.5-transform['offset_x' if i%2==0 else 'offset_y'])/
                    transform['scale_x' if i%2==0 else 'scale_y'] for i in range(4)]
        expected = np.clip(expected,0,[width,height,width,height])
        np.testing.assert_allclose(candidate['bbox'],expected,rtol=0,atol=1e-4)
        assert candidate['class']=='person' and candidate['score']==.25
        assert float(objects[0,index].sigmoid()*classes[0,index,0].sigmoid())==.25
        # Padding-only responses cannot become non-empty native target boxes.
        for head in heads:
            head[:,4:]=-80
        assert decode_heads(heads,transform)==[]
    print('PASS: 4 source aspect ratios, independent decoder/native transforms, empty candidates')


if __name__=='__main__':
    main()
