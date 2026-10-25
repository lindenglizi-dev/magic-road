"""Four fixed real-parameter layers; CPU goldens and logical WIF1 transactions.

No torch import, GPU, training, RTL execution, synthesis, or board operation.
Existing producer tensors are CPU reference assets, not a running RTL prefix.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
PRODUCTION = HERE.parents[1]
PROJECT = PRODUCTION.parents[2]
sys.path.insert(0, str(PROJECT))
from cnn.integer import conv2d, requantize, silu, tables

PACKAGE = PROJECT / "cnn/reports/qat_frozen_stem_g10_20261014_v1/package"
FAMILY = PRODUCTION / "csp_family_layer_scheduled_20261015/reference"
PREFIX = PRODUCTION / "model_handoff_20261015/artifacts/golden_prefix"
PAYLOAD = "b35d4a66a69e441dc29bc60c7e3f507661f48da5f33b810d7340f6ed17a65145"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def emit(path, values, bits):
    path.parent.mkdir(parents=True, exist_ok=True)
    mask = (1 << bits) - 1
    path.write_text("".join(f"{int(value) & mask:0{(bits + 3) // 4}x}\n" for value in values), encoding="ascii")


def pack(values, bits):
    return sum((int(value) & ((1 << bits) - 1)) << (bits * lane) for lane, value in enumerate(values))


def address(node, y, x, channel):
    h, w, c = node["output_shape_hwc"]
    assert 0 <= y < h and 0 <= x < w and 0 <= channel < c
    pixel = ((y // 4) * ((w + 3) // 4) + x // 4) * 16 + (y % 4) * 4 + x % 4
    return node["storage"]["base"] + pixel * c + channel


def quant(params, channels):
    return (pack([params["bias"][c] for c in channels], 32)
            | pack([params["pre_multiplier"][c] for c in channels], 32) << 96
            | pack([params["pre_shift"][c] for c in channels], 6) << 192
            | int(params["post_multiplier"][0]) << 210
            | int(params["post_shift"][0]) << 242)


def parameters(node, payload, segments):
    result = {}
    for item in node["parameters"]:
        segment = segments[node["name"] + "." + item["field"]]
        assert (segment["offset"], segment["length"]) == (item["byte_offset"], item["length"])
        raw = payload[segment["offset"]:segment["offset"] + segment["length"]]
        assert hashlib.sha256(raw).hexdigest() == segment["sha256"]
        dtype = "i1" if item["field"] == "weights" else ("u1" if "shift" in item["field"] else "<i4")
        result[item["field"]] = np.frombuffer(raw, dtype=dtype).copy()
    cout = node["output_shape_hwc"][2]
    cin = node["input_shape_hwc"][2] // node["groups"]
    result["weights"] = result["weights"].reshape(cout, cin, *node["kernel"])
    return result


def execute(node, source, params, conv_exact):
    assert source.dtype == np.int8 and list(source.shape) == node["input_shape_hwc"]
    acc = conv_exact(source, params["weights"], params["bias"], node["stride"][0], node["padding"][0], node["groups"])
    pre = requantize(acc, params["pre_multiplier"], params["pre_shift"], -32768, 32767).astype(np.int16)
    activated = silu(pre)
    post = requantize(activated, params["post_multiplier"], params["post_shift"]).astype(np.int8)
    return {"acc": acc, "pre": pre, "silu": activated, "post": post}


def schedule(node, source_node, source, params, expected, root):
    """Generate scheduling independently of the scalar-convolution oracle."""
    h, w, cout = node["output_shape_hwc"]
    cin = node["input_shape_hwc"][2]
    dw = node["groups"] > 1
    tiles = [(0, 0), (0, w - 4), (((h - 1) // 4) * 4, 0), (((h - 1) // 4) * 4, w - 4), ((h // 8) * 4, (w // 8) * 4)]
    cases = []
    for case_id, (y0, x0) in enumerate(tiles):
        case = root / f"tile_{case_id}_y{y0}_x{x0}"
        case.mkdir(parents=True, exist_ok=True)
        tasks, groups, trace, weights, quants = [], [], [], [], []
        byte_writes, byte_reads, weight_writes, weight_reads = [], [], [], []
        fill_addresses=[]
        selected = range(cin) if dw else range(0, cout, 3)
        for channel in selected:
            if dw:
                store = [int(source[y0 * 2 - 1 + r, x0 * 2 - 1 + c, channel])
                         if 0 <= y0 * 2 - 1 + r < source.shape[0] and 0 <= x0 * 2 - 1 + c < source.shape[1] else 0
                         for r in range(9) for c in range(9)]
                channels = [channel] * 3
                banks = []
                for window in (7, 3):
                    union = 3 * window
                    for group in range((union + 7) // 8):
                        lane_weights = []
                        for lane in range(3):
                            for k in range(8):
                                n = group * 8 + k
                                ky, ux = divmod(n, window)
                                kx = ux - lane * 2
                                lane_weights.append(int(params["weights"][channel, 0, ky, kx])
                                                    if n < union and 0 <= kx < 3 and (window == 7 or lane == 0) else 0)
                        banks.append({"window": window, "group": group, "slot": len(banks), "weight192": pack(lane_weights, 8)})
            else:
                store = [int(source[y0 + r, x0 + c, k]) if y0 + r < h else 0
                         for r in range(4) for c in range(4) for k in range(cin)]
                channels = [channel + lane for lane in range(3)]
                banks = [{"window": 0, "group": group, "slot": group,
                          "weight192": pack([params["weights"][oc, group * 8 + k, 0, 0]
                                             for oc in channels for k in range(8)], 8)} for group in range(cin // 8)]
            assert len(store) <= 3072 and len(banks) <= 24
            q = quant(params, channels)
            quants.append(q)
            if dw or channel==0:
                for local, value in enumerate(store):
                    trace.append(("byte", 1, local, value & 255, 0))
                    byte_writes.append((local << 8) | (value & 255))
                    if dw:
                        fy,fx=y0*2-1+local//9,x0*2-1+local%9
                        fc=channel
                    else:
                        pixel,fc=divmod(local,cin)
                        fy,fx=y0+pixel//4,x0+pixel%4
                    fill_addresses.append(address(source_node,fy,fx,fc) if 0<=fy<source.shape[0] and 0<=fx<source.shape[1] else 0xffffffff)
            for bank in banks:
                trace.append(("weight", 1, bank["slot"], bank["weight192"], 0))
                weight_writes.append((bank["slot"] << 192) | bank["weight192"])
                weights.append({"channel": channel, **bank, "quant248": q})
            # Check every emitted tile/channel against the existing scalar oracle.
            if dw:
                patch = np.array(store, dtype=np.int8).reshape(9, 9, 1)
                scalar = conv2d(patch, params["weights"][channel:channel + 1], params["bias"][channel:channel + 1], stride=2)
                assert np.array_equal(scalar[:min(4, h-y0), :, 0], expected["acc"][y0:min(y0+4,h), x0:x0+4, channel])
            else:
                patch = np.array(store, dtype=np.int8).reshape(4, 4, cin)
                scalar = conv2d(patch, params["weights"][channel:channel + 3], params["bias"][channel:channel + 3])
                assert np.array_equal(scalar[:min(4, h-y0)], expected["acc"][y0:min(y0+4,h), x0:x0+4, channel:channel+3])
            positions = [(r, c) for r in range(min(4, h-y0)) for c in ((0, 3) if dw else range(4))]
            for r, c in positions:
                window = (7 if c == 0 else 3) if dw else 0
                active = 3 if not dw or c == 0 else 1
                task_id = len(tasks)
                dst = [address(node, y0+r, x0+c+(lane if dw else 0), channel if dw else channels[lane]) if lane < active else 0 for lane in range(3)]
                outputs = [[int(expected[field][y0+r, x0+c+(lane if dw else 0), channel if dw else channels[lane]]) if lane < active else 0 for lane in range(3)] for field in ("acc", "pre", "silu", "post")]
                task = {"task": task_id, "channel": channel, "r": r, "c": c, "window": window,
                        "mask": (1 << active)-1, "quant248": q, "addresses": dst,
                        **dict(zip(("acc", "pre", "silu", "post"), outputs)), "first_group": len(groups)}
                running = [int(params["bias"][channels[lane]]) if lane < active else 0 for lane in range(3)]
                selected_banks = [bank for bank in banks if bank["window"] == window]
                for index, bank in enumerate(selected_banks):
                    count = min(8, (3*window if dw else cin)-bank["group"]*8)
                    offsets = []
                    for k in range(count):
                        n = bank["group"] * 8 + k
                        if dw:
                            ky, ux = divmod(n, window)
                            offsets.append((r*2+ky)*9+c*2+ux)
                        else:
                            offsets.append((r*4+c)*cin+n)
                    values = [store[offset] for offset in offsets] + [0]*(8-count)
                    trace.append(("weight", 0, bank["slot"], 0, bank["weight192"]))
                    weight_reads.append((bank["slot"] << 192) | bank["weight192"])
                    for offset in offsets:
                        trace.append(("byte", 0, offset, 0, store[offset] & 255))
                        byte_reads.append((offset << 8) | (store[offset] & 255))
                    raw_weight = bank["weight192"].to_bytes(24, "little")
                    for lane in range(active):
                        running[lane] += sum(values[k] * (raw_weight[lane*8+k] if raw_weight[lane*8+k]<128 else raw_weight[lane*8+k]-256) for k in range(count))
                        assert -(1 << 32) <= running[lane] < (1 << 32)
                    groups.append({"task": task_id, "slot": bank["slot"], "first": int(index == 0),
                                   "last": int(index == len(selected_banks)-1), "mask": (1 << count)-1,
                                   "activation64": pack(values, 8), "weight192": bank["weight192"],
                                   "offsets": offsets, "acc33": running.copy()})
                assert running == outputs[0], (node["name"], y0, x0, task)
                task["group_count"] = len(selected_banks)
                tasks.append(task)
        memory={"byte":{},"weight":{}}
        for port,write,offset,data,response in trace:
            assert 0<=offset<(3072 if port=="byte" else 24)
            if write:
                assert response==0
                memory[port][offset]=data
            else:
                assert data==0 and offset in memory[port] and memory[port][offset]==response
        assert len({dst for row in tasks for lane,dst in enumerate(row["addresses"]) if row["mask"]&(1<<lane)}) == min(4,h-y0)*4*cout
        save(case / "tasks.json", tasks)
        save(case / "parameter_responses.json", weights)
        for field, bits in (("activation64",64),("weight192",192),("first",1),("last",1),("mask",8),("slot",5)):
            emit(case / ("group_"+field+".hex"), (row[field] for row in groups), bits)
        emit(case / "group_offsets96.hex", (pack(row["offsets"]+[0]*(8-len(row["offsets"])),12) for row in groups),96)
        emit(case / "group_acc99.hex", (pack(row["acc33"],33) for row in groups),99)
        emit(case / "weight_writes197.hex", weight_writes,197)
        emit(case / "weight_reads197.hex", weight_reads,197)
        emit(case / "byte_writes20.hex", byte_writes,20)
        emit(case / "byte_reads20.hex", byte_reads,20)
        emit(case / "fill_source_addresses32.hex",fill_addresses,32)
        emit(case / "output_writes40.hex",((row["addresses"][lane]<<8)|(row["post"][lane]&255) for row in tasks for lane in range(3) if row["mask"]&(1<<lane)),40)
        emit(case / "parameter_quant248.hex", quants,248)
        for field,bits in (("acc",32),("pre",16),("silu",16),("post",8),("addresses",32),("mask",1)):
            emit(case / ("task_"+field+".hex"), (row[field] if field=="mask" else pack(row[field],bits) for row in tasks),3 if field=="mask" else bits*3)
        with (case / "wif1_transactions.csv").open("w",encoding="ascii",newline="") as stream:
            writer=csv.writer(stream)
            writer.writerow(["sequence","channel","write","address_or_group","request_hex","response_hex","error"])
            writer.writerows((n,*row[:3],f"{row[3]:x}",f"{row[4]:x}",0) for n,row in enumerate(trace))
        cases.append({"case":case_id,"tile_y":y0,"tile_x":x0,"valid_rows":min(4,h-y0),"tasks":len(tasks),"groups":len(groups),"directory":str(case.relative_to(HERE)).replace("\\","/"),"wif1_transactions":len(trace)})
    return cases


def main():
    graph_path = PRODUCTION / "graph_artifacts/graph.json"
    remaining_path = PRODUCTION / "rom_two_client_20261015/remaining_layers.json"
    manifest_path = PACKAGE / "manifest.json"
    payload_path = PACKAGE / "numeric_test.bin"
    graph, remaining, manifest = read(graph_path), read(remaining_path), read(manifest_path)
    assert sha(graph_path) == remaining["graph_sha256"]
    assert sha(manifest_path) == remaining["manifest_sha256"]
    assert sha(payload_path) == manifest["payload_sha256"] == PAYLOAD
    payload = payload_path.read_bytes()
    segments = {item["name"]:item for item in manifest["segments"]}
    lut = segments["shared.silu"]
    lut_bytes = payload[lut["offset"]:lut["offset"]+lut["length"]]
    assert hashlib.sha256(lut_bytes).hexdigest() == lut["sha256"]
    assert np.array_equal(np.frombuffer(lut_bytes,dtype="<i2"),tables()["silu"])
    # Reuse the exact existing NumPy convolution function without importing its torch calibration module.
    trained_path = PRODUCTION / "trained_integer.py"
    tree = ast.parse(trained_path.read_text(encoding="utf-8"))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "conv_exact")
    namespace = {"np":np}
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(trained_path), "exec"),namespace)
    source2 = PREFIX / "csp2.out.conv.post.npy"
    source3 = FAMILY / "csp3/npy/stage6_output.npy"
    family_manifest = read(FAMILY / "manifest.json")
    assert sha(source2) == "58787fb0627e18aaadf6fe35385e90f2253da6acb82b4efff49a02fc8b69701e"
    assert sha(source3) == family_manifest["artifacts"]["csp3/npy/stage6_output.npy"]
    sources = {12:np.load(source2,allow_pickle=False),26:np.load(source3,allow_pickle=False)}
    layers=[]
    parameter_rows=[]
    for layer_id in (12,13,26,27):
        node=next(item for item in remaining["layers"] if item["graph_index"] == layer_id)
        assert graph["nodes"][layer_id]["name"] == node["name"]
        params=parameters(node,payload,segments)
        source=sources[layer_id]
        result=execute(node,source,params,namespace["conv_exact"])
        if layer_id in (13,27):
            prior=FAMILY / ("csp3/npy/source.npy" if layer_id==13 else "csp4/npy/source.npy")
            assert sha(prior) == family_manifest["artifacts"][str(prior.relative_to(FAMILY)).replace("\\","/")]
            assert np.array_equal(result["post"],np.load(prior,allow_pickle=False))
        root=HERE / node["name"]
        root.mkdir(parents=True,exist_ok=True)
        emit(root / "input_hwc8.hex",source.ravel(),8)
        for field,bits in (("acc",32),("pre",16),("silu",16),("post",8)):
            emit(root / ("expected_hwc_"+field+".hex"),result[field].ravel(),bits)
        save(root / "parameters.json",{name:value.tolist() for name,value in params.items()})
        source_node=next(item for item in graph["nodes"] if item.get("output")==node["inputs"][0])
        cases=schedule(node,source_node,source,params,result,root)
        for row in read(HERE / cases[0]["directory"] / "parameter_responses.json"):
            parameter_rows.append({"layer_id":layer_id,**row})
        layers.append({"layer_id":layer_id,"name":node["name"],"input_shape_hwc":node["input_shape_hwc"],"output_shape_hwc":node["output_shape_hwc"],"storage":node["storage"],"cases":cases})
        if layer_id in (12,26):
            sources[layer_id+1]=result["post"]
    inputs=[graph_path,remaining_path,manifest_path,payload_path,trained_path,PROJECT/"cnn/integer.py",source2,source3,FAMILY/"manifest.json",Path(np.__file__),Path(sys.executable),Path(__file__)]
    inputs += [FAMILY/"csp3/npy/source.npy",FAMILY/"csp4/npy/source.npy"]
    inputs += list({Path(module.__file__) for name,module in sys.modules.items()
                    if name.startswith("numpy") and getattr(module,"__file__",None)})
    binding={str(path):sha(path) for path in inputs}
    closure=hashlib.sha256(json.dumps(binding,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    save(HERE / "tasks.json",{"status":"CPU_REFERENCE_ONLY_REAL_G10_PARAMETERS","payload_sha256":PAYLOAD,"closure_sha256":closure,"layers":layers})
    save(HERE / "input_binding.json",{"closure_sha256":closure,"source_sha256":binding,"python":sys.version,"numpy":np.__version__,"boundary":"CPU producer tensors and four CPU layers; representative tile schedule only; no RTL/full-prefix/31-layer execution, DDR, physical mapping, timing, QAT or accuracy claim"})
    save(HERE / "remaining31_index.json",remaining)
    save(HERE / "parameter_responses.json",parameter_rows)
    assert len(parameter_rows)==600
    assert len({(row["layer_id"],row["channel"],row["window"],row["group"]) for row in parameter_rows})==600
    emit(HERE / "parameter_requests22.hex",((row["layer_id"]<<15)|(row["channel"]<<8)|(row["window"]<<5)|row["group"] for row in parameter_rows),22)
    emit(HERE / "parameter_weight192.hex",(row["weight192"] for row in parameter_rows),192)
    emit(HERE / "parameter_quant248.hex",(row["quant248"] for row in parameter_rows),248)
    save(HERE / "verification_receipt.json",{"status":"PASS","layers":4,"tiles":20,"tasks":sum(case["tasks"] for layer in layers for case in layer["cases"]),"groups":sum(case["groups"] for layer in layers for case in layer["cases"]),"scalar_oracle":"Every emitted tile/channel accumulator equals cnn.integer.conv2d; every grouped signed33 reduction equals full conv_exact result","closure_sha256":closure})
    artifacts={str(path.relative_to(HERE)).replace("\\","/"):sha(path) for path in HERE.rglob("*") if path.is_file() and path.name != "artifact_manifest.json" and "__pycache__" not in path.parts}
    save(HERE / "artifact_manifest.json",artifacts)
    print(json.dumps(read(HERE / "verification_receipt.json")))


if __name__ == "__main__":
    main()
