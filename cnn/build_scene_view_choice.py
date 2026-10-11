"""Build an offline scene preference sheet, not a dataset or annotation editor."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "cnn/reports/scene_view_choice_20261009_v1"
SCENES = [
    {"id": "A", "title": "固定斜俯视 · 道路通道 / 出入口", "recommendation": "优先主场景",
     "description": "理想取景是看清中近处人车与连续通道。本地暂缺理想的简单园区通道代表图，A1只有宽路口里的直路布局参考，不是推荐照搬的全景。",
     "benefit": "便于设越线、通行方向和禁入区；比贴地顺路看更容易分开前后目标。",
     "risk": "仍可能互相遮挡；远端目标仍会变小。应先靠实际取景控制范围，不承诺此视角必然达标。"},
    {"id": "B", "title": "低机位 / 近地斜视 · 街边与人行通道", "recommendation": "可选主场景或补充",
     "description": "目标外观较完整、近处目标大，但前后目标易相互挡住。本批无严格水平平视道路代表图；B1/B2只是低至中位斜视行人场景参考。",
     "benefit": "若摄像头只能低位安装，或需要看清人体/车体外观，可以保留。",
     "risk": "多人/多车排队时易漏检、换ID、重复计数；顺着很长的道路看，远端尤其困难。"},
    {"id": "C", "title": "固定斜俯视 · 停车场 / 园区空地", "recommendation": "建议只把通道作为业务区域",
     "description": "视野宽、几何边界较清楚，但大量静止车不等于车流量。",
     "benefit": "适合通道越线、区域占用、禁入区；人车混行可作为后续扩展。",
     "risk": "全场静止车可能占满每类32框的输出槽；只在显示端隐藏ROI外框不会让CNN省计算或自动腾出槽。"},
    {"id": "D", "title": "高处斜俯视 · 多车道 / 大路口", "recommendation": "后续扩展或压力对照",
     "description": "覆盖多条车道、转弯、骑行者和远端行人。并非不能做，而是第一版业务规则更复杂。",
     "benefit": "适合后续按车道分别统计方向和流量。",
     "risk": "小远目标、遮挡和目标数量同时增加；全局一个方向箭头不能解释双向车道和转弯。"},
    {"id": "E", "title": "无人机航拍 · 高空斜视 / 近俯视", "recommendation": "对照项，不默认作为主训练域",
     "description": "与固定地面监控不是同一种部署方式；本地无人机样图也不等于严格垂直正俯视。",
     "benefit": "可看整体通行布局，保留为历史回归和视角对照。",
     "risk": "目标可能极小；摄像头运动还会改变图像轨迹。固定图像计数线不能直接套到移动机位。"},
    {"id": "F", "title": "固定正俯视 · 几乎垂直向下", "recommendation": "需要真实安装条件与新的代表图",
     "description": "本批不把高处斜视照片冒充正俯视。若你选择这一项，再针对性找固定顶视视频。",
     "benefit": "小范围通道的地面位置关系可能更直观，前后遮挡形式也不同。",
     "risk": "人体外观会变成头肩为主；面积扩大后目标变小。仍需匹配此视角训练，不能直接认为现有模型更准。"},
]

CORE = r'''
const SceneChoiceCore = (() => {
  const roles = new Set(["pending", "primary", "secondary", "stress", "exclude"]);
  const events = ["line_count", "occupancy", "trajectory", "wrong_way", "zone_entry", "metric_risk"];
  const defaults = () => ({scene_roles:Object.fromEntries("ABCDEF".split("").map(k=>[k,"pending"])),
    camera:"pending", density:"pending", lighting:"pending", events:[], notes:""});
  function valid(s) {
    return !!s && typeof s === "object" && !!s.scene_roles && Object.keys(s.scene_roles).sort().join("")==="ABCDEF" &&
      Object.values(s.scene_roles).every(x=>roles.has(x)) &&
      ["pending","choose_fixed","fixed_locked","replay"].includes(s.camera) &&
      ["pending","low","medium","low_medium","high"].includes(s.density) &&
      ["pending","day","day_night","all_weather"].includes(s.lighting) &&
      Array.isArray(s.events) && s.events.every(x=>events.includes(x)) && new Set(s.events).size===s.events.length &&
      typeof s.notes==="string" && s.notes.length<=4000;
  }
  function makeExport(s, sourceHash, now) {
    if (!valid(s) || !/^[a-f0-9]{64}$/.test(sourceHash)) throw Error("选择格式无效");
    return {schema:"roadyolo_scene_preferences_v1", status:"preference_draft_not_data_freeze",
      source_manifest_sha256:sourceHash, exported_at:now, preferences:JSON.parse(JSON.stringify(s)),
      training_started:false, labels_changed:false, acceptance_changed:false};
  }
  function recommendation(s, confirmed) {
    if (valid(confirmed)) return {...JSON.parse(JSON.stringify(confirmed)), notes:s.notes};
    return {...s, scene_roles:{A:"primary",B:"secondary",C:"secondary",D:"stress",E:"stress",F:"pending"},
      density:s.density==="pending"?"medium":s.density, lighting:s.lighting==="pending"?"day":s.lighting,
      events:s.events.length?s.events:["line_count","trajectory","wrong_way","zone_entry"]};
  }
  return {defaults, valid, makeExport, recommendation};
})();
globalThis.SceneChoiceCore = SceneChoiceCore;
'''

PAGE = r'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>RoadYOLO · 视角与场景选择册</title>
<style>
:root{color-scheme:light dark;--bg:light-dark(#f6f7fa,#13161b);--panel:light-dark(#fff,#1d232b);--ink:light-dark(#202733,#edf1f7);--muted:light-dark(#49576b,#b5c3d6);--line:light-dark(#cbd3df,#475368);--accent:light-dark(#134d85,#a5ccff)}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 "Microsoft YaHei",system-ui,sans-serif}main{max-width:1180px;margin:auto;padding:24px}h1{font-size:27px;margin:0}h2{font-size:22px;margin:28px 0 12px}h3{font-size:19px;margin:0}p{margin:10px 0}a{color:var(--accent)}button,input,select,textarea{font:inherit;color:var(--ink)}button,select,textarea{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:8px 12px}button{cursor:pointer}button:focus-visible,select:focus-visible,a:focus-visible,textarea:focus-visible{outline:3px solid var(--accent);outline-offset:3px}button:disabled{cursor:not-allowed}label{display:block}small,.meta{font-size:14px;color:var(--muted)}.box{padding:16px;background:var(--panel);border:1px solid var(--line);border-radius:10px;margin:14px 0}.toolbar{display:flex;gap:12px;flex-wrap:wrap;align-items:center}.formgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}.formgrid select{width:100%}.photos{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}.photos figure{margin:0;min-width:0}.photos img{display:block;width:100%;height:auto;border-radius:5px}.photos img.network{width:512px;max-width:100%;border-radius:0}figcaption{margin-top:6px;font-size:14px;overflow-wrap:anywhere}.scenehead{display:flex;justify-content:space-between;gap:12px;align-items:center;flex-wrap:wrap}.tag{font-size:14px;color:var(--accent)}table{width:100%;border-collapse:collapse}th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:10px}thead{background:var(--panel)}.scroll{overflow:auto}textarea{width:100%;min-height:80px}.checks{display:flex;gap:18px;flex-wrap:wrap}.checks label{display:flex;align-items:center;gap:6px;min-height:44px}.checks input{width:18px;height:18px}details{margin:10px 0}summary{cursor:pointer;min-height:38px}#status{min-height:28px}#saveError{color:light-dark(#9c1a22,#ffb5bd)}@media(max-width:600px){main{padding:14px}.photos{grid-template-columns:1fr}h1{font-size:23px}th,td{padding:7px}}
</style></head><body><main>
<h1>RoadYOLO · 视角与场景选择册</h1>
<p>只选“希望系统用于什么场景”，<strong>不需要逐框标注</strong>。所有图片均为真实本地样图，无GT框、教师框或模型预测。</p>
<div class="box"><strong>建议起点：固定斜俯视 + 中近距离通道 + 白天低中密度。</strong>
<p>平视和俯视都能用于计数、轨迹、逆行，但视角会影响遮挡、可见目标大小和位置估计；不是完全无关。先选贴近实际部署的取景，再决定数据与训练，不靠挑容易视频宣称普遍达标。</p>
<p class="meta">分类是目视判断，不是实测相机高度/倾角，也不是训练资格认证。样图本身已经被查看，只能作开发/选择参考，不能再宣称是未见盲测。</p></div>
<div class="toolbar"><button id="recommend" type="button">填入建议组合（可修改）</button><button id="export" type="button">导出我的选择</button><a href="场景选择说明与后续步骤.txt">完整说明与后续步骤</a></div>
<p id="status" role="status" aria-live="polite">尚未选择；推荐项不会自动当作你的决定。</p><p id="saveError" role="alert"></p>
<h2>一、对照照片，给每类选用途</h2>
<p>只需定1—2类主场景；其余可选补充、压力对照、暂不考虑或保留未决定。可直接在聊天里回复类别编号，不必导出。</p>
<div id="scenes"></div>
<h2>二、补充实际条件</h2>
<div class="formgrid">
<label>摄像头安装条件<select id="camera"><option value="pending">未决定</option><option value="choose_fixed">可以自行选固定机位</option><option value="fixed_locked">已有固定机位，不能改</option><option value="replay">当前只回放公开视频</option></select></label>
<label>主要业务区域的目标密度<select id="density"><option value="pending">未决定</option><option value="low">稀疏（约人0–5、车0–10）</option><option value="medium">中等（约人6–15或车11–20）</option><option value="low_medium">低中密度（应用偏好，未冻结数量边界）</option><option value="high">更密集 / 可能超过每类32个</option></select></label>
<label>第一阶段光照范围<select id="lighting"><option value="pending">未决定</option><option value="day">白天 / 正常光照</option><option value="day_night">白天 + 夜间</option><option value="all_weather">还需要雨雾 / 强逆光</option></select></label>
</div><p class="meta">密度区间仅帮助描述偏好，不是实测能力或新验收门槛。每类32个上限针对完整帧，不只针对业务ROI。若必须覆盖夜雨，不能只用白天样图作为证据。</p>
<p>想优先实现的业务（可多选；选择不代表这些功能已经实现）：</p>
<div class="checks" id="events"><label><input type="checkbox" value="line_count">越线流量计数</label><label><input type="checkbox" value="occupancy">区域当前人数 / 车数</label><label><input type="checkbox" value="trajectory">轨迹与ID保持</label><label><input type="checkbox" value="wrong_way">分车道 / 分区域逆行</label><label><input type="checkbox" value="zone_entry">禁入区 / 人车混行提示</label><label><input type="checkbox" value="metric_risk">真实距离 / 速度 / 碰撞风险（另需标定与时序验证）</label></div>
<label for="notes">补充，例如“只看近端两条车道、不统计停车位”</label><textarea id="notes" maxlength="4000" placeholder="可不填；不要在这里填写逐框标注"></textarea>
<h2>三、不同任务真正需要什么</h2>
<div class="scroll"><table><thead><tr><th>任务</th><th>视角的影响</th><th>还缺什么，不能只靠检测框</th></tr></thead><tbody>
<tr><td>区域当前数量</td><td>遮挡会少数；重复框会多数；高处广角会把远处目标缩小。</td><td>完整框、区域归属规则、去重；不要把静止车辆数当车流量。</td></tr>
<tr><td>越线流量</td><td>贴地顺路视角易前后遮挡；固定斜俯视通常较便于看通道。</td><td>连续视频、稳定ID、跨线方向、迟滞/去重；静态图片AP不能证明计数正确。</td></tr>
<tr><td>轨迹</td><td>低位遮挡、远端小目标、移动机位都更容易断轨。</td><td>连续时间戳、漏帧处理与跟踪验证。CNN输出框不等于已有跟踪。</td></tr>
<tr><td>逆行</td><td>平视/俯视都可；图像向上不天然等于道路正向。</td><td>每个车道/区域的允许方向、持续位移判断；双向和转弯分别定义。只判方向不一定需要米制标定。</td></tr>
<tr><td>预警</td><td>图像框相交不等于地面碰撞；视角和道路坡度影响距离。</td><td>先做规则型禁入/混行提示。真实距离、速度和TTC需标定、接地点/道路平面假设、端到端延迟与误报漏报验证；不作安全保证。</td></tr>
</tbody></table></div>
<div class="box"><strong>与板子规格的关系</strong><p>保持同一512×288网络时，换视角本身不改变卷积数量和权重容量。密度影响Top-K/NMS负载、每类32框上限和后续跟踪状态；跟踪/事件模块的资源仍需另行设计与实测。</p>
<p>5 FPS只是目标，相邻检测名义间隔约200 ms；500 ms是旧结果撤框阈值，不是预警安全反应时间保证。显示画面流畅不等于检测每帧更新。</p>
<p>不靠删除小目标GT提分。若业务只覆盖中近距离，应先冻结业务ROI及边界规则，仍单列全帧原口径结果。当前ROI外目标仍可占输出槽；前置ROI过滤如要实现，需另行评估，不能仅在画框端隐藏。</p></div>
<h2>四、选择后怎么推进</h2>
<ol><li>你选主场景、安装条件和优先事件；本页只记录偏好，不冻结数据。</li><li>按所选视角找完整人车标注的训练/开发候选，确认骑行者人体与车体、机位/原片划分；不会让你重新审核所有Ground48。</li><li>冻结开发口径，先评E7，再启动有明确预算与保护的G100；无收益先定位，不自动追加训练。</li><li>检测稳定后再做视频跟踪/越线/逆行验证；量化、RTL和正式验收仍按现有门槛推进。</li></ol>
<details><summary>来源、许可与证据边界</summary><div id="sources"></div><p>照片仅在本机用于本项目场景讨论，不自动授权再分发。SPD8为已查看开发对照，其机位不进入训练。Intersection的场景/相机映射和完整标签资格仍待核查；目视同场景不证明正式camera_id。CDnet仅作视角样例，不能当完整人车GT。</p><p id="bindings" class="meta"></p></details>
<script id="manifest" type="application/json">__MANIFEST__</script>
<script id="core">__CORE__</script>
<script id="app">
(() => {
  const M=JSON.parse(document.getElementById("manifest").textContent), C=globalThis.SceneChoiceCore;
  const key="roadyolo_scene_view_choice_20261009_v1"+(M.confirmed_preference_sha256?"_"+M.confirmed_preference_sha256:""), $=id=>document.getElementById(id);
  let state=M.confirmed_preferences?JSON.parse(JSON.stringify(M.confirmed_preferences)):C.defaults();
  if(M.confirmed_preferences) textConfirmed();
  function textConfirmed(){const p=document.createElement("p");p.className="box";p.textContent="聊天中已确认：主A、补充C、D压力对照；白天低中密度、机位可自选；优先计数/轨迹/逆行。下方是可编辑草稿，可能恢复你后来修改的内容，与上述确认不同；导出不会覆盖确认记录。";$("scenes").before(p);$("recommend").textContent="恢复已确认组合（保留备注）";}
  try {const saved=JSON.parse(localStorage.getItem(key)||"null"); if(C.valid(saved)) state=saved;} catch(e) {$("saveError").textContent="浏览器未允许保存；仍可选择并导出。";}
  function text(tag,value,parent,className="") {const x=document.createElement(tag); x.textContent=value;if(className)x.className=className;parent.append(x);return x;}
  for (const s of M.scenes) {
    const section=document.createElement("section");section.className="box";$("scenes").append(section);
    const header=document.createElement("div");header.className="scenehead";section.append(header);
    const titles=document.createElement("div");header.append(titles);text("h3",s.id+" · "+s.title,titles);text("span",s.recommendation,titles,"tag");
    const label=text("label","这一类的用途：",header),select=document.createElement("select");select.id="role-"+s.id;select.dataset.scene=s.id;
    for (const [v,t] of [["pending","未决定"],["primary","主场景"],["secondary","补充场景"],["stress","压力对照"],["exclude","暂不考虑"]]) {const o=document.createElement("option");o.value=v;o.textContent=t;select.append(o);}label.append(select);
    text("p",s.description,section);text("p","适合点："+s.benefit,section);text("p","注意："+s.risk,section);
    const photos=document.createElement("div");photos.className="photos";section.append(photos);
    const rows=M.photos.filter(p=>p.scene===s.id);
    if(!rows.length) text("p","本批无可靠代表图，保留该选项，不拿别的视角冒充。",photos,"meta");
    for (const p of rows) {
      const f=document.createElement("figure");photos.append(f);const a=document.createElement("a");a.href=p.original_url;a.target="_blank";a.rel="noopener";f.append(a);
      const img=document.createElement("img");img.src=p.display_file;img.alt=p.photo_id+"："+p.caption;img.loading="lazy";a.append(img);
      const cap=text("figcaption",p.photo_id+" · "+p.caption,f);text("div",p.source+" · "+p.source_role+" · "+p.width+"×"+p.height,cap,"meta");
      text("div",p.boundary,cap,"meta");const raw=text("a","打开无框原图",cap);raw.href=p.original_url;raw.target="_blank";raw.rel="noopener";
      const detail=document.createElement("details");f.append(detail);text("summary","看512×288网络输入（无推理）",detail);
      const n=document.createElement("img");n.src=p.network_file;n.alt=p.photo_id+" 按现有数据预处理生成的512×288输入，无预测";n.className="network";n.loading="lazy";detail.append(n);
      text("small","按现有letterbox到720p→精确2/5缩放，只帮助看目标实际像素；不是识别结果。",detail);
    }
  }
  for(const s of M.sources){const p=document.createElement("p");$("sources").append(p);const a=text("a",s.title,p);a.href=s.url;a.target="_blank";a.rel="noopener";text("span"," — "+s.scope,p);}
  $("bindings").textContent="照片清单SHA256："+M.photo_manifest_sha256+"；选择状态不是训练授权，也不改变正式验收。";
  function put(){for(const s of M.scenes)$("role-"+s.id).value=state.scene_roles[s.id];for(const id of ["camera","density","lighting","notes"])$(id).value=state[id];$("events").querySelectorAll("input").forEach(x=>x.checked=state.events.includes(x.value));status();}
  function collect(){const s=C.defaults();for(const scene of M.scenes)s.scene_roles[scene.id]=$("role-"+scene.id).value;for(const id of ["camera","density","lighting","notes"])s[id]=$(id).value;s.events=Array.from($("events").querySelectorAll("input:checked"),x=>x.value);return s;}
  function status(){const ids=Object.entries(state.scene_roles).filter(([k,v])=>v==="primary").map(([k])=>k);$("status").textContent=ids.length?"当前主场景："+ids.join("、")+"；只是偏好草稿，尚未冻结训练或验收口径。":"尚未选择主场景；可继续对照照片，或直接在聊天里告诉我编号。";}
  function save(){state=collect();if(!C.valid(state))throw Error("选择格式无效");try{localStorage.setItem(key,JSON.stringify(state));}catch(e){$("saveError").textContent="选择未能写入浏览器；请导出保存。";}status();}
  document.querySelectorAll("select,textarea,#events input").forEach(x=>x.addEventListener("change",save));$("notes").addEventListener("input",save);
  $("recommend").addEventListener("click",()=>{state=C.recommendation(collect(),M.confirmed_preferences);put();save();});
  $("export").addEventListener("click",()=>{try{save();const blob=new Blob([JSON.stringify(C.makeExport(state,M.photo_manifest_sha256,new Date().toISOString()),null,2)],{type:"application/json"});const a=document.createElement("a"),url=URL.createObjectURL(blob);a.href=url;a.download="scene_preferences_"+Date.now()+".json";document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);$("status").textContent="已请求导出偏好草稿；请把下载文件发回聊天。未启动训练。";}catch(e){$("saveError").textContent=e.message;}});
  put();
})();
</script></main></body></html>
'''


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare_photos():
    """Only load explicitly selected train/development originals; never inspect labels."""
    import numpy as np
    from PIL import Image
    try:
        from .dataset import _letterbox_720
        from .integer import resize_area
    except ImportError:
        from dataset import _letterbox_720
        from integer import resize_area

    candidates_file = OUT / "candidates/candidates.json"
    candidates = json.loads(candidates_file.read_text(encoding="utf-8"))
    candidates_by_id = {p["candidate_id"]: p for p in candidates["candidates"]}
    assert len(candidates_by_id) == len(candidates["candidates"])
    selection_file = OUT / "photo_selection.json"
    selected = json.loads(selection_file.read_text(encoding="utf-8"))
    assert 6 <= len(selected) <= 20
    assert len({p["id"] for p in selected}) == len(selected)
    allowed_roots = [ROOT / p for p in [
        "cnn/data/intersection_flow_5k/raw_v4/Intersection-Flow-5K/images/train",
        "cnn/reports/post_review_s_20261007_v1/ground48/images",
        "cnn/reports/replacement48_spd_draft8_20261008_v2/raw",
        "cnn/data/visdrone_vid_train/extracted/VisDrone2019-VID-train/sequences",
        "public_data/raw/cdnet_pedestrian/dataset/pedestrian detection dataset/busStation/input",
        "public_data/raw/cdnet_pedestrian/dataset/pedestrian detection dataset/pedestrians/input",
    ]]
    (OUT / "network_inputs").mkdir(exist_ok=True)
    photos = []
    for choice in selected:
        row = candidates_by_id[choice["id"]]
        original = Path(row["original_path"]).resolve()
        assert any(original.is_relative_to(p.resolve()) for p in allowed_roots), original
        assert row["split_role"] in {"train", "development-reviewed", "train-view-example", "train-development-view"}
        assert digest(original) == row["sha256"], original
        assert re.fullmatch(r"[a-z0-9_]+", choice["id"])
        assert choice["scene"] in "ABCDEF"
        with Image.open(original) as image:
            assert list(image.size) == row["size"]
            rgb = np.asarray(image.convert("RGB"))
        canvas, transform = _letterbox_720(rgb)
        resized = resize_area(canvas)
        target = OUT / "network_inputs" / (choice["id"] + ".png")
        Image.fromarray(resized).save(target)
        thumb = Path(row["thumbnail_path"]).resolve()
        assert thumb.is_relative_to((OUT / "candidates").resolve()) and thumb.is_file()
        photos.append({
            "photo_id": choice["photo_id"], "candidate_id": choice["id"], "scene": choice["scene"],
            "caption": choice["caption"], "boundary": choice["boundary"],
            "source": row["source"], "source_role": row["split_role"],
            "known_source": row["known_source"], "visual_class": row["visual_class"],
            "original_path": str(original), "original_url": original.as_uri(),
            "source_sha256": row["sha256"], "width": row["size"][0], "height": row["size"][1],
            "display_file": thumb.relative_to(OUT.resolve()).as_posix(),
            "network_file": target.relative_to(OUT).as_posix(), "network_sha256": digest(target),
            "preprocess_transform": transform,
        })
    sources = [
        {"title": "Intersection-Flow-5K 本地README", "url": (ROOT / "cnn/data/intersection_flow_5k/raw_v4/Intersection-Flow-5K/README.md").as_uri(),
         "scope": "train样图；本地README声明CC BY-NC-SA 4.0，来源绑定、机位和完整GT资格仍待核实。"},
        {"title": "VIRAT 官方站点", "url": "https://viratdata.org/", "scope": "只复用已经查看的Ground48原图；原GT未完成状态不改变。"},
        {"title": "SPD 用户已下载官方示例", "url": "https://drive.google.com/file/d/1gjOmGEBMcipvDzu2zOrO9ex_OscUZMYY/view", "scope": "已查看SPD8辅助样图；示例包许可范围仍待核实，不据此授权再分发或训练。"},
        {"title": "CDnet 官方来源", "url": "https://changedetection.net/dataset2014/", "scope": "只取train的busStation/pedestrians；低至中位斜视示例，不是完整人车GT。"},
        {"title": "VisDrone 官方项目", "url": "https://github.com/VisDrone/VisDrone-Dataset", "scope": "train航拍对照，不是固定道路验收。"},
        {"title": "UA-DETRAC 检测与跟踪论文", "url": "https://arxiv.org/abs/1511.04136", "scope": "遮挡、尺度、检测与多目标跟踪的关系；不证明本工程选定视角的精度。"},
        {"title": "OpenCV 官方单应性教程", "url": "https://docs.opencv.org/4.13.0/d9/dab/tutorial_homography.html", "scope": "平面透视映射的前提；本项目未做现场米制标定。"},
        {"title": "MOTChallenge 视频跟踪评测", "url": "https://arxiv.org/abs/1504.01942", "scope": "视频与跨帧关联独立评测，不能用静态AP代替事件验证。"},
    ]
    manifest = {
        "schema": "roadyolo_scene_photo_manifest_v1", "purpose": "preference_selection_only_not_training_GT",
        "training_started": False, "model_inference_run": False, "labels_modified": False,
        "source_read_boundary": candidates["source_read_boundary"], "uncovered_views": candidates["uncovered_views"],
        "candidate_manifest_sha256": digest(candidates_file), "selection_sha256": digest(selection_file),
        "preprocess_source_sha256": {p: digest(ROOT / p) for p in ["cnn/dataset.py", "cnn/integer.py"]},
        "photos": photos, "sources": sources,
    }
    (OUT / "photo_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def check():
    """Validate the exact generated assets plus preference serialization behavior."""
    manifest = json.loads((OUT / "photo_manifest.json").read_text(encoding="utf-8"))
    assert 6 <= len(manifest["photos"]) <= 20
    assert len({p["photo_id"] for p in manifest["photos"]}) == len(manifest["photos"])
    assert {p["scene"] for p in manifest["photos"]} <= set("ABCDEF")
    for p in manifest["photos"]:
        assert p["source_role"] not in {"test", "blind", "reserve", "newtest"}
        source = Path(p["original_path"])
        assert not re.search(r"(^|[/\\])(test|blind[^/\\]*|[^/\\]*reserve[^/\\]*|newtest[^/\\]*)([/\\]|$)", str(source), re.I)
        assert digest(source) == p["source_sha256"], source
        for key in ("display_file", "network_file"):
            path = (OUT / p[key]).resolve()
            assert path.is_relative_to(OUT.resolve()) and path.is_file(), path
        from PIL import Image
        with Image.open(OUT / p["network_file"]) as image:
            assert image.size == (512, 288)
        assert digest(OUT / p["network_file"]) == p["network_sha256"]
    for p, expected in manifest["preprocess_source_sha256"].items():
        assert digest(ROOT / p) == expected, p
    assert digest(OUT / "candidates/candidates.json") == manifest["candidate_manifest_sha256"]
    assert digest(OUT / "photo_selection.json") == manifest["selection_sha256"]
    text = (OUT / "index.html").read_text(encoding="utf-8")
    scripts = dict(re.findall(r'<script id="([^"]+)"(?: type="[^"]+")?>(.*?)</script>', text, re.S))
    assert {"manifest", "core", "app"} == set(scripts)
    embedded = json.loads(scripts["manifest"])
    assert embedded["photo_manifest_sha256"] == digest(OUT / "photo_manifest.json")
    assert embedded["photos"] == manifest["photos"]
    confirmed_file = OUT / "confirmed_preferences.json"
    if confirmed_file.exists():
        confirmed = json.loads(confirmed_file.read_text(encoding="utf-8"))
        assert confirmed["status"] == "user_confirmed_scene_preferences_not_dataset_freeze"
        assert confirmed["source_manifest_sha256"] == digest(OUT / "photo_manifest.json")
        assert embedded["confirmed_preference_sha256"] == digest(confirmed_file)
        assert embedded["confirmed_preferences"] == confirmed["preferences"]
        assert not any(confirmed[k] for k in ("training_started", "labels_changed", "acceptance_changed", "dataset_frozen"))
    syntax = subprocess.run(["node", "--check", "-"], input=scripts["core"] + scripts["app"],
                            text=True, encoding="utf-8", capture_output=True)
    assert syntax.returncode == 0, syntax.stderr
    tests = r'''
const assert=require('node:assert/strict'), C=globalThis.SceneChoiceCore, s=C.defaults();
assert.ok(C.valid(s)); assert.ok(Object.values(s.scene_roles).every(x=>x==='pending'));
s.scene_roles.A='primary'; s.events=['line_count','wrong_way']; assert.ok(C.valid(s));
s.density='low_medium'; assert.ok(C.valid(s));
const e=C.makeExport(s,'a'.repeat(64),'2026-10-09T00:00:00Z');
assert.equal(e.status,'preference_draft_not_data_freeze'); assert.equal(e.training_started,false);
assert.equal(e.labels_changed,false); assert.equal(e.acceptance_changed,false);
s.scene_roles.A='exclude'; assert.equal(e.preferences.scene_roles.A,'primary');
assert.equal(C.valid({...s,events:['unknown']}),false);
assert.equal(C.valid({...s,events:['line_count','line_count']}),false);
assert.equal(C.valid({...s,notes:'x'.repeat(4001)}),false);
assert.equal(C.valid({...s,scene_roles:{A:'primary'}}),false);
assert.throws(()=>C.makeExport(C.defaults(),'bad','now'));
console.log('PASS preference defaults, validation, immutable draft export');
'''
    result = subprocess.run(["node", "-"], input=CORE + tests, text=True, encoding="utf-8", capture_output=True)
    assert result.returncode == 0, result.stderr
    print(result.stdout.strip())
    if confirmed_file.exists():
        confirmed_tests = "\nconst confirmed=" + json.dumps(confirmed["preferences"], ensure_ascii=False) + r''';
const assert=require('node:assert/strict'), C=SceneChoiceCore;
assert.ok(C.valid(confirmed));
const draft=C.defaults(); draft.notes='keep my note'; draft.scene_roles.B='primary';
const restored=C.recommendation(draft,confirmed);
assert.deepEqual(restored.scene_roles,confirmed.scene_roles);
assert.deepEqual(restored.events,['line_count','trajectory','wrong_way']);
assert.equal(restored.notes,'keep my note');
restored.scene_roles.A='exclude'; assert.equal(confirmed.scene_roles.A,'primary');
assert.equal(C.recommendation(C.defaults(),null).scene_roles.A,'primary');
console.log('PASS confirmed choices, restoration, preserved notes, no extra events');
'''
        result = subprocess.run(["node", "-"], input=CORE + confirmed_tests, text=True, encoding="utf-8", capture_output=True)
        assert result.returncode == 0, result.stderr
        print(result.stdout.strip())
    print(f"PASS {len(manifest['photos'])} source hashes, local assets, 512x288 inputs and JavaScript syntax")


def build():
    prepare_photos()
    source = OUT / "photo_manifest.json"
    manifest = json.loads(source.read_text(encoding="utf-8"))
    embedded = {**manifest, "scenes": SCENES, "photo_manifest_sha256": digest(source)}
    confirmed_file = OUT / "confirmed_preferences.json"
    if confirmed_file.exists():
        confirmed = json.loads(confirmed_file.read_text(encoding="utf-8"))
        if confirmed["source_manifest_sha256"] != digest(source):
            raise ValueError("Confirmed preferences belong to a different photo manifest")
        embedded["confirmed_preferences"] = confirmed["preferences"]
        embedded["confirmed_preference_sha256"] = digest(confirmed_file)
    payload = json.dumps(embedded, ensure_ascii=False).replace("<", "\\u003c")
    page = PAGE.replace("__MANIFEST__", payload).replace("__CORE__", CORE)
    (OUT / "index.html").write_text(page, encoding="utf-8")
    check()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    check() if args.check else build()
