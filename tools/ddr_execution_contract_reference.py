#!/usr/bin/env python3
"""DDR 待接入合同的可运行参考：在途预算、取消、背景身份与 ROI 边界。

这是约束检查与确定性向量，不模拟 DDR IP、CDC、显示 FIFO 或真实延迟。
"""
from __future__ import annotations

import argparse
import json
from collections import deque
from pathlib import Path

import numpy as np

from candidate_chain_reference import digest
from ddr_detection_capacity_probe import PROJECT
from local_paired_diagnostic import dump
from roi_dataset_tool import fpga_gray_bgr, fpga_resize_roi


class ReturnBudget:
    """单个接收缓存的拍数预留；本合同假定同通道请求顺序返回。"""
    def __init__(self, depth, owner_slots):
        if depth < 1 or owner_slots < 1:
            raise ValueError('positive FIFO depth and owner queue size required')
        self.depth, self.owner_slots = depth, owner_slots
        self.occupied = self.reserved = 0
        self.pending = deque()
        self.serial = 0

    def check(self):
        assert 0 <= self.occupied and 0 <= self.reserved
        assert self.occupied+self.reserved <= self.depth
        assert self.reserved == sum(r['left'] for r in self.pending)
        assert len(self.pending) <= self.owner_slots

    def accept(self, beats, valid=True, ready=True):
        if beats < 1:
            raise ValueError('positive response length required')
        if not valid or not ready:
            return None
        if len(self.pending) == self.owner_slots or self.occupied+self.reserved+beats > self.depth:
            return None
        self.serial += 1
        self.pending.append({'id':self.serial,'left':beats,'discard':False})
        self.reserved += beats
        self.check()
        return self.serial

    def cancel(self):
        # 已接受返回不能消失：标记丢弃但保留归属和预留至最后一拍。
        for request in self.pending:
            request['discard'] = True
        self.check()

    def receive(self, request_id):
        if not self.pending or self.pending[0]['id'] != request_id:
            raise ValueError('unexpected, duplicate or out-of-order return')
        request = self.pending[0]
        request['left'] -= 1
        self.reserved -= 1
        if not request['discard']:
            self.occupied += 1
        if not request['left']:
            self.pending.popleft()
        self.check()

    def consume(self, beats):
        if beats < 0 or beats > self.occupied:
            raise ValueError('receive FIFO underflow')
        self.occupied -= beats
        self.check()

    def reset_after_drain(self):
        if self.pending or self.occupied:
            raise ValueError('reset requires accepted returns and old FIFO contents to drain')
        self.check()


def commit_decision(input_complete, update_complete, write_complete, quality_passed,
                    ccl_success, normal_background=True, separate_commit_enabled=False):
    """独立背景提交只能在受控实验中显式启用；显示延迟不是背景质量条件。"""
    trustworthy = input_complete and update_complete and write_complete and quality_passed
    return {'background_commit': bool(trustworthy and normal_background and
                                     (ccl_success or separate_commit_enabled)),
            'detection_success': bool(trustworthy and ccl_success and normal_background)}


def source_half_open(box, stride):
    xmin,ymin,xmax,ymax = box
    if stride not in (2,5) or not 0 <= xmin <= xmax < 1280//stride or not 0 <= ymin <= ymax < 720//stride:
        raise ValueError('invalid analysis box')
    return xmin*stride, ymin*stride, (xmax+1)*stride, (ymax+1)*stride


def next_display_commit(ready_ns, period_ns):
    if ready_ns < 0 or period_ns < 1:
        raise ValueError('invalid timestamp')
    # 边界包含在预算内；实际建立时间必须计入 ready_ns 的准备段。
    return ((ready_ns+period_ns-1)//period_ns)*period_ns


def task_trace(compute_ns, prepare_ns, release_ns, count=12):
    """理想 60 Hz / 单任务、显示 ACK 后重启的算术例子；不是实测调度。"""
    period = 16_666_667
    source_period = 41_708_333  # 仅示例中的约 23.976 Hz；正式用真实捕获时间戳。
    if min(compute_ns,prepare_ns,release_ns) < 0:
        raise ValueError('negative duration')
    rows, start, background_version = [], 0, 0
    for task in range(count):
        if rows:
            start = max(start, (rows[-1]['source_frame_id']+1)*source_period)
        source_id = start//source_period
        source_time = source_id*source_period
        ready = start+compute_ns
        commit = next_display_commit(ready+prepare_ns,period)
        next_start = commit+release_ns
        rows.append({'task_id':task,'source_frame_id':source_id,'source_timestamp_ns':source_time,
                     'background_version_used':background_version,'task_start_ns':start,
                     'result_ready_ns':ready,'display_commit_ns':commit,'next_task_start_ns':next_start,
                     'result_age_at_display_ns':commit-source_time,'failure_reason':None})
        background_version += 1
        start = next_start
    return rows


def self_check():
    budget = ReturnBudget(8,2)
    assert budget.accept(4,valid=False) is None and budget.accept(4,ready=False) is None
    first,second = budget.accept(5),budget.accept(3)
    assert budget.accept(1) is None and budget.reserved==8
    budget.receive(first)
    assert (budget.occupied,budget.reserved)==(1,7)
    budget.cancel()
    assert budget.reserved==7  # 取消不释放在途预留。
    try:
        budget.reset_after_drain()
    except ValueError:
        pass
    else:
        raise AssertionError('reset lost pending traffic')
    for _ in range(4):
        budget.receive(first)
    for _ in range(3):
        budget.receive(second)
    assert budget.occupied==1 and budget.reserved==0
    budget.consume(1); budget.reset_after_drain()
    try:
        budget.receive(second)
    except ValueError:
        pass
    else:
        raise AssertionError('duplicate return accepted')
    decision=commit_decision(True,True,True,True,False,separate_commit_enabled=True)
    assert decision=={'background_commit':True,'detection_success':False}
    assert not commit_decision(True,True,False,True,True)['background_commit']
    assert not commit_decision(True,True,False,True,True)['detection_success']
    assert not commit_decision(True,False,True,True,True)['detection_success']
    assert not commit_decision(False,True,True,True,True)['detection_success']
    assert not commit_decision(True,True,True,False,True)['detection_success']
    assert not commit_decision(True,True,True,False,False,separate_commit_enabled=True)['background_commit']
    assert not commit_decision(True,True,True,True,True,normal_background=False)['detection_success']
    assert source_half_open((639,359,639,359),2)==(1278,718,1280,720)
    assert source_half_open((255,143,255,143),5)==(1275,715,1280,720)
    assert source_half_open((0,0,639,359),2)==(0,0,1280,720)
    edge_bgr=np.full((2,2,3),255,np.uint8)
    assert (fpga_gray_bgr(edge_bgr)==253).all()
    corners=np.array([[10,20],[30,40]],np.uint8)
    golden=np.repeat(np.repeat(corners,16,axis=0),16,axis=1)
    assert np.array_equal(fpga_resize_roi(corners),golden)
    identity=np.arange(1024,dtype=np.uint16).reshape(32,32)
    assert np.array_equal(fpga_resize_roi(identity),identity)
    gray=np.arange(720*1280,dtype=np.uint32).reshape(720,1280)%254
    bounds=source_half_open((252,140,255,143),5)
    x0,y0,x1,y1=bounds
    crop=gray[y0:y1,x0:x1].astype(np.uint8)
    centers=np.minimum(((2*np.arange(32)+1)*20)//64,19)
    assert np.array_equal(fpga_resize_roi(crop),crop[np.ix_(centers,centers)])
    fast=task_trace(45_000_000,1_000_000,2_000_000)
    slow=task_trace(45_000_000,5_000_000,2_000_000)
    assert fast[2]['display_commit_ns']-fast[1]['display_commit_ns']==3*16_666_667
    assert slow[2]['display_commit_ns']-slow[1]['display_commit_ns']==4*16_666_667
    immediate=task_trace(1_000_000,1_000_000,1_000_000)
    assert len({r['source_frame_id'] for r in immediate})==len(immediate)
    return {'status':'PASS_reference_only','fifo_cancel_and_reset':'PASS',
            'background_separate_validity':'PASS','roi_boundary_gray_and_dda':'PASS',
            'illustrative_task_traces':{'three_vsync_periods':fast,'four_vsync_periods':slow}}


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=self_check()
    if args.output:
        out=args.output.resolve()
        if out.exists() or not out.is_relative_to((PROJECT/'evaluation/ddr_architecture').resolve()):
            raise ValueError('choose fresh output within DDR diagnostics')
        out.mkdir(parents=True)
        dump(out/'reference_checks.json',report)
        dump(out/'receipt.json',{'script_sha256':digest(Path(__file__)),
            'roi_reference_sha256':digest(PROJECT/'tools/roi_dataset_tool.py'),
            'report_sha256':digest(out/'reference_checks.json'),
            'boundary':'software assertions and ideal timestamp examples, not RTL/DDR/CDC validation'})
    print(json.dumps({k:v for k,v in report.items() if k!='illustrative_task_traces'},ensure_ascii=False,indent=2))
