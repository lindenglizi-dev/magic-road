#!/usr/bin/env python3
"""Bit-exact reference for Lesson09.
Input SCORE is raw signed INT32 dot product. One row at a time.
scale_q16 approximates 1/sqrt(D) in unsigned Q16.
Negative difference in Q4 is floored (arithmetic right shift).
Exp LUT Q16 = round(exp(-j/16)*65535), j=0..128.
Score delta below -8 is clamped to zero exp weight.
Output unsigned uint8: nearest integer of 255*exp/sum(exp) (ties rounded up).
Note sum(uint8) is not guaranteed to equal 255.
"""
import math
import numpy as np

LUT = tuple(int(math.floor(65535.0 * math.exp(-j/16.0) + 0.5)) for j in range(129))
assert LUT[0] == 65535

def scale_for_dim(d):
    if d < 1 or d > 256:
        raise ValueError(d)
    return int(math.floor(65536.0/math.sqrt(d)+0.5))

def approximate_exp_weights(row, scale_q16):
    vals = [int(x) for x in row]
    assert 1 <= len(vals) <= 64
    vmax = max(vals)
    out=[]
    for score in vals:
        # the raw score difference is exactly signed 33-bit in hardware
        diff_q4 = ((score-vmax)*int(scale_q16)) >> 12
        j=-diff_q4
        out.append(LUT[j] if 0<=j<=128 else 0)
    return out

def softmax_fixed(row, scale_q16):
    weights = approximate_exp_weights(row, scale_q16)
    total = sum(weights)
    assert total >= 65535 and total <= 64*65535
    return [min(255, (255*x + total//2)//total) for x in weights]

def softmax_float(row, d):
    vals = np.asarray(row,dtype=np.float64)/math.sqrt(d)
    z=np.exp(vals-vals.max()); return 255*(z/z.sum())

if __name__ == '__main__':
    s=[[14,8],[2,-11]]
    print('score:',s, 'scale_q16:',scale_for_dim(4))
    print('fixed u8:',[softmax_fixed(row,scale_for_dim(4)) for row in s])
    print('float*255:',[softmax_float(row,4).round(3).tolist() for row in s])
