"""Reuse the frozen tile scheduler and package; never run old vector writers."""
import importlib.util
import json
import shutil
from execute import HERE, REPORTS, check, sha, write

check()
v = REPORTS/'v19_mac_short_closure_20261008'
r = REPORTS/'v8_reset_layer_tiles_20261007/layers/reference.py'
package = HERE.parents[1]/'numeric_artifacts/numeric_test.bin'
desc = REPORTS/'fixed_graph_function_20261008/fixed_layer_descriptors.json'
sources = [r,package,desc,v/'rtl/down2_overlap_tile_runner.v',v/'rtl/road_mac_probe.v']
input_hashes={str(p):sha(p) for p in sources}
if (HERE/'layer_inputs.json').exists():
    assert json.loads((HERE/'layer_inputs.json').read_text())==input_hashes
else:
    write(HERE/'layer_inputs.json',input_hashes)
d=HERE/'layer'
(d/'rtl').mkdir(parents=True,exist_ok=True)
(d/'vectors').mkdir(exist_ok=True)
for old,new in [('down2_overlap_tile_runner.v','down2_dynamic_tile_runner.v'),('road_mac_probe.v','road_mac_probe.v')]:
    if (d/'rtl'/new).exists():
        assert sha(d/'rtl'/new)==sha(v/'rtl'/old)
    else:
        shutil.copy2(v/'rtl'/old,d/'rtl'/new)
spec=importlib.util.spec_from_file_location('frozen_reference',r)
ref=importlib.util.module_from_spec(spec)
spec.loader.exec_module(ref)
payload=package.read_bytes()
descriptors=json.loads(desc.read_text(encoding='utf-8'))
assert sha(package)==descriptors['payload_sha256']
layers=descriptors['layers'][1:3]
assert [x['name'] for x in layers]==['down2.dw.conv','down2.pw.conv']

def read(offset,n,width,signed):
    return [int.from_bytes(payload[offset+i*width:offset+(i+1)*width], 'little',signed=signed) for i in range(n)]

params=[]
for layer in layers:
    f=layer['field_offsets']; cout=layer['output_hwc'][2]
    pre=read(f['pre_multiplier'],cout,4,True); shifts=read(f['pre_shift'],cout,1,False)
    post=read(f['post_multiplier'],1,4,True)[0]; postshift=read(f['post_shift'],1,1,False)[0]
    assert set(pre)=={65536} and set(shifts)=={24} and post==16777216 and postshift==31
    params.append({'pre':pre,'pre_shift':shifts,'post':post,'post_shift':postshift})
ref.dw_weights=lambda:read(layers[0]['field_offsets']['weights'],144,1,True)
ref.dw_biases=lambda:read(layers[0]['field_offsets']['bias'],16,4,True)
ref.pw_weights=lambda:read(layers[1]['field_offsets']['weights'],384,1,True)
ref.pw_biases=lambda:read(layers[1]['field_offsets']['bias'],24,4,True)
def quant(acc,slot):
    pre=ref.round_shift(acc*65536,24)
    act=ref.silu(pre)
    post=ref.round_shift(act*16777216,31)
    return pre,act,post,ref.sat8(post)
ref.quantize=quant
# Full-range deterministic activations prevent the weak old fixture collapsing.
ref.activation=lambda row,col,ch: ((row*97+col*53+ch*31)%256)-128
def hexfile(name,values,width):
    mask=(1<<width)-1
    contents=''.join(f'{x&mask:0{width//4}x}\n' for x in values)
    if (d/'vectors'/name).exists():
        assert (d/'vectors'/name).read_text(encoding='ascii')==contents
        return
    with (d/'vectors'/name).open('x',encoding='ascii') as out:
        out.write(contents)
for name,values,width in [('silu.hex',ref.SILU,16),('dw_weights.hex',ref.dw_weights(),8),
                          ('dw_biases.hex',ref.dw_biases(),32),('pw_weights.hex',ref.pw_weights(),8),('pw_biases.hex',ref.pw_biases(),32)]:
    hexfile(name,values,width)
cases=[]
for name,origin in [('edge',(0,0)),('interior',(20,32)),('bottom_right',(68,124))]:
    halo,padding=ref.halo(*origin)
    dw,dwr=ref.depthwise(halo)
    pw,pwr=ref.pointwise(dw)  # PW consumes NEW quantized DW, not an old accumulator.
    hexfile(name+'_halo.hex',halo,8)
    hexfile(name+'_output.hex',pw,8)
    records=sorted(dwr+pwr,key=lambda x:(x['layer'],x['position'],x['channel']))
    hexfile(name+'_acc.hex',[x['acc'] for x in records],32)
    hexfile(name+'_commit.hex',[x['output'] for x in records],32)
    target=d/'vectors'/(name+'_records.json')
    if target.exists():
        assert json.loads(target.read_text())==records
    else:
        write(target,records)
    assert len(records)==640 and len(set(dw))>1
    cases.append({'name':name,'output_origin':origin,'padding_bytes':padding,
                  'dw_distinct':len(set(dw)),'pw_distinct':len(set(pw)),'scalar_records':640,
                  'weak_final_fixture':len(set(pw))==1})
write(d/'vectors/manifest.json',{'status':'TEST_PACKAGE_NOT_DEPLOYMENT_QAT',
      'cases':cases,'parameter_values':params,'layout':'4x4 HWC, all origins aligned',
      'counts':{'halo':1296,'weight_bias':568,'silu_load':1024,'dw_commits':256,'pw_commits':384},
      'files':{p.name:sha(p) for p in (d/'vectors').iterdir() if p.is_file()}})
assert all(sha(__import__('pathlib').Path(p))==h for p,h in json.loads((HERE/'layer_inputs.json').read_text()).items())
check()
print('LAYER_REFERENCE_PASS',json.dumps(cases))
