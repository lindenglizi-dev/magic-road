"""One authorized five-update head-only branch from frozen-Stem QAT G10."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time
from types import SimpleNamespace

import numpy as np
import torch

from cnn.hw_validation.production import train_qat as base
from cnn.hw_validation.production import train_qat_frozen_stem as frozen
from cnn.hw_validation.production import train_qat_frozen_stem_continue as continuation
from cnn.hw_validation.production import train_qat_numpy235 as runtime
from cnn.hw_validation.production.diagnose_qat_continuation_drift import head_layout
from cnn.hw_validation.production.qat_exact import QATExactModel
from cnn.hw_validation.production.run_trained_integer import centered, save
from cnn.hw_validation.production.trained_integer import load_package, write_package
from cnn.train import protocol_hash, restore_rng, rng_state, sha256, _state_equal


OUT = base.PROJECT / "cnn/reports/qat_head_only_g5_20261014_v1"
RUN = base.PROJECT / "cnn/runs/qat_head_only_g5_20261014_v1"
CHECK_DIR = OUT / "integration_check_v1"
AUTHORIZATION = OUT / "user_authorization.json"
AUTHORIZATION_SHA256 = "d6abe3511d03c75fc9cd214fba13cb16f615c1fb7db0a04669e288c5d21e5312"
FORMAT = "road-qat-head-only-g5-v1"
UPDATES = 5
PRIOR_GLOBAL_UPDATES = 30
GLOBAL_UPDATES = PRIOR_GLOBAL_UPDATES + UPDATES
WORKER_MODULE = "cnn.hw_validation.production.train_qat_head_only"
PARENT = continuation.PARENT
PARENT_SHA256 = continuation.PARENT_SHA256


def _tensor_sha256(value: torch.Tensor) -> str:
    return hashlib.sha256(value.detach().cpu().contiguous().numpy().tobytes()).hexdigest()


def parameter_contract(parent: dict, graph: dict) -> tuple[list[str], list[str], list[dict]]:
    _roots, head_layers = head_layout(graph)
    head_set = set(head_layers)
    convs = [node["name"] for node in graph["nodes"] if node["op"] == "conv"]
    trainable = [f"layers.{index}.{field}" for index, name in enumerate(convs)
                 if name in head_set for field in ("weight", "bias")]
    frozen_names = [f"layers.{index}.{field}" for index, name in enumerate(convs)
                    if name not in head_set for field in ("weight", "bias")]
    parent_names = [f"layers.{index}.{field}" for index, name in enumerate(convs)
                    if name != "stem.conv" for field in ("weight", "bias")]
    group = parent["optimizer"]["param_groups"]
    slots = parent["optimizer"]["state"]
    if len(group) != 1 or len(group[0]["params"]) != 132 or len(parent_names) != 132:
        raise ValueError("parent optimizer/name cardinality changed")
    by_name = dict(zip(parent_names, group[0]["params"], strict=True))
    mapping = []
    for current_slot, name in enumerate(trainable):
        parent_slot = by_name[name]
        state = slots.get(parent_slot, {})
        momentum = state.get("momentum_buffer")
        if set(state) != {"momentum_buffer"} or momentum is None:
            raise ValueError(f"missing parent momentum: {name}")
        if tuple(momentum.shape) != tuple(parent["model"][name].shape) or not torch.isfinite(momentum).all():
            raise ValueError(f"invalid parent momentum: {name}")
        mapping.append({"name": name, "parent_optimizer_slot": int(parent_slot),
                        "head_optimizer_slot": current_slot, "shape": list(momentum.shape),
                        "dtype": str(momentum.dtype),
                        "momentum_sha256": _tensor_sha256(momentum)})
    if len(trainable) != 42 or len(frozen_names) != 92 or len(mapping) != 42:
        raise ValueError("expected 21 head and 46 frozen non-head convolutions")
    return trainable, frozen_names, mapping


def prepare():
    if os.environ.get("PYTORCH_NVML_BASED_CUDA_CHECK") != "1":
        raise ValueError("PYTORCH_NVML_BASED_CUDA_CHECK must be 1")
    if sha256(AUTHORIZATION) != AUTHORIZATION_SHA256:
        raise ValueError("user authorization receipt changed")
    authorization = base.read(AUTHORIZATION)
    if (authorization.get("parent_checkpoint_sha256") != PARENT_SHA256
            or authorization.get("planned_new_candidate_optimizer_updates") != UPDATES
            or authorization.get("global_qat_candidate_updates_after_completion") != GLOBAL_UPDATES
            or authorization.get("rejected_G20_used_as_parent") is not False
            or authorization.get("automatic_retry") is not False
            or authorization.get("automatic_continuation") is not False):
        raise ValueError("authorization scope changed")
    dataset, window, folded, runtime_identity, _runtime_protocol, _runtime_ancestry, parent = runtime.prepare()
    if sha256(PARENT) != PARENT_SHA256 or parent.get("trained_steps") != 10:
        raise ValueError("frozen-Stem G10 parent changed")
    integer, _ = load_package(base.BASE / "package")
    trainable, frozen_names, mapping = parameter_contract(parent, integer.graph)
    protocol = dict(parent["training_protocol"],
        name="deployment_exact_qat_head_only_g5_v1", total_updates=UPDATES,
        local_update_labels=[f"H{index}" for index in range(UPDATES + 1)],
        source_schedule_updates=[index + 1 for index in range(UPDATES)],
        source_global_update_numbers=[index + 11 for index in range(UPDATES)],
        prior_global_qat_updates=PRIOR_GLOBAL_UPDATES,
        global_qat_updates_after_segment=GLOBAL_UPDATES,
        overall_budget_cap=100, frozen_nonhead_convolutions=46,
        trainable_head_convolutions=21, trainable_parameter_tensors=42,
        frozen_parameter_tensors=92,
        gradient_clipping_scope="trainable_head_parameters_only_changes_effective_head_clip_gain",
        cpu_resume_check_threads=2, gpu_worker_threads=2,
        pytorch_nvml_based_cuda_check="1", additional_ram_hard_threshold=False,
        automatic_retry=False, automatic_continuation=False)
    identity = dict(parent["identity"], numpy_version=np.__version__,
        experiment_id="qat_head_only_g5_20261014_v1",
        protocol_sha256=protocol_hash(protocol), native_runtime=runtime_identity["native_runtime"],
        runtime_transition=runtime_identity["runtime_transition"],
        authorization_receipt_sha256=AUTHORIZATION_SHA256,
        parent_checkpoint_sha256=PARENT_SHA256,
        parent_identity_sha256=protocol_hash(parent["identity"]),
        parent_training_protocol_sha256=protocol_hash(parent["training_protocol"]),
        parent_sample_history_sha256=protocol_hash(parent["sample_history"]),
        trainable_parameter_names=trainable, frozen_parameter_names=frozen_names,
        optimizer_name_mapping=mapping, optimizer_name_mapping_sha256=protocol_hash(mapping))
    identity["source_sha256"] = dict(runtime_identity["source_sha256"])
    for path in (Path(__file__), Path(__file__).with_name("test_train_qat_head_only.py"),
                 Path(__file__).with_name("diagnose_qat_continuation_drift.py")):
        identity["source_sha256"][str(path.relative_to(base.PROJECT)).replace("\\", "/")] = sha256(path)
    ancestry = dict(parent_checkpoint=str(PARENT.relative_to(base.PROJECT)).replace("\\", "/"),
        parent_checkpoint_sha256=PARENT_SHA256, parent_trained_steps=10,
        parent_presentations=220, parent_identity=copy.deepcopy(parent["identity"]),
        parent_training_protocol=copy.deepcopy(parent["training_protocol"]),
        parent_sample_history=copy.deepcopy(parent["sample_history"]),
        parent_rng_state=copy.deepcopy(parent["rng_state"]))
    return dataset, window, folded, identity, protocol, ancestry, parent


def model_and_optimizer(folded, device, parent, identity):
    model = frozen.FrozenStemQAT.from_package(
        base.BASE / "package", folded, base.BASE / "quantization.json")
    model.load_state_dict(parent["model"], strict=True)
    model.to(device)
    trainable = set(identity["trainable_parameter_names"])
    named = dict(model.named_parameters())
    for name, parameter in named.items():
        parameter.requires_grad_(name in trainable)
    ordered = [(name, parameter) for name, parameter in model.named_parameters() if parameter.requires_grad]
    if [name for name, _ in ordered] != identity["trainable_parameter_names"]:
        raise ValueError("head parameter order changed")
    optimizer = torch.optim.SGD((parameter for _, parameter in ordered),
                                lr=1e-4, momentum=.9, weight_decay=5e-4)
    parent_slots = parent["optimizer"]["state"]
    for row, (name, parameter) in zip(identity["optimizer_name_mapping"], ordered, strict=True):
        if row["name"] != name:
            raise ValueError("optimizer name mapping changed")
        momentum = parent_slots[row["parent_optimizer_slot"]]["momentum_buffer"]
        if list(momentum.shape) != row["shape"] or _tensor_sha256(momentum) != row["momentum_sha256"]:
            raise ValueError("parent momentum mapping changed")
        optimizer.state[parameter]["momentum_buffer"] = momentum.detach().to(device).clone()
    return model, optimizer


def sample_record(dataset, window, local_update):
    row = base.sample_record(dataset, window, local_update)
    row.update(local_update=local_update + 1, local_update_label=f"H{local_update + 1}",
               source_schedule_update=local_update + 1, source_global_update=local_update + 11)
    return row


def update_once(model, optimizer, dataset, window, local_update, device, pause=None):
    record = base.update_once(model, optimizer, dataset, window, local_update, device, pause)
    if record is not None:
        record.update(local_update=local_update + 1, local_update_label=f"H{local_update + 1}",
                      source_schedule_update=local_update + 1, source_global_update=local_update + 11)
    return record


def _optimizer_ok(state, mapping):
    groups, slots = state.get("param_groups"), state.get("state")
    expected = [row["head_optimizer_slot"] for row in mapping]
    return (isinstance(groups, list) and len(groups) == 1 and groups[0].get("params") == expected
            and groups[0].get("lr") == 1e-4 and groups[0].get("momentum") == .9
            and groups[0].get("weight_decay") == 5e-4 and groups[0].get("dampening") == 0
            and groups[0].get("nesterov") is False and groups[0].get("maximize") is False
            and set(slots or {}) == set(expected) and len(slots) == 42
            and all(set(slots[index]) == {"momentum_buffer"}
                    and list(slots[index]["momentum_buffer"].shape) == row["shape"]
                    and str(slots[index]["momentum_buffer"].dtype) == row["dtype"]
                    and torch.isfinite(slots[index]["momentum_buffer"]).all()
                    for index, row in enumerate(mapping)))


def checkpoint(model, optimizer, identity, protocol, ancestry, history, *, candidate):
    count = len(history)
    return dict(format=FORMAT, checkpoint_kind="training", phase="qat", candidate=candidate,
        identity=identity, training_protocol=protocol, ancestry=copy.deepcopy(ancestry),
        optimizer_name_map=copy.deepcopy(identity["optimizer_name_mapping"]),
        model=model.state_dict(), optimizer=optimizer.state_dict(), rng_state=rng_state(),
        trained_steps=count, next_update=count, local_trained_steps=count,
        next_local_update=count, local_update_label=f"H{count}", presentations=count * 22,
        global_qat_updates=PRIOR_GLOBAL_UPDATES + count,
        sample_history=copy.deepcopy(history), actual_samples_per_update=22,
        gradients_pending=False, formal_acceptance=False)


def validate_state(state, identity, protocol, ancestry, parent, dataset, window, *, candidate):
    count = state.get("local_trained_steps")
    if (state.get("format") != FORMAT or state.get("checkpoint_kind") != "training"
            or state.get("phase") != "qat" or state.get("candidate") is not candidate
            or state.get("formal_acceptance") is not False or state.get("identity") != identity
            or state.get("training_protocol") != protocol
            or not _state_equal(state.get("ancestry"), ancestry)
            or state.get("optimizer_name_map") != identity["optimizer_name_mapping"]
            or type(count) is not int or not 0 <= count <= UPDATES
            or state.get("trained_steps") != count or state.get("next_update") != count
            or state.get("next_local_update") != count or state.get("local_update_label") != f"H{count}"
            or state.get("presentations") != count * 22
            or state.get("global_qat_updates") != PRIOR_GLOBAL_UPDATES + count
            or state.get("actual_samples_per_update") != 22 or state.get("gradients_pending") is not False
            or len(state.get("sample_history", [])) != count
            or not _optimizer_ok(state.get("optimizer", {}), identity["optimizer_name_mapping"])
            or set(state.get("rng_state", {})) != {"python", "numpy", "torch", "cuda"}):
        raise ValueError("head-only identity, ancestry, optimizer or cursor mismatch")
    for index, actual in enumerate(state["sample_history"]):
        expected = sample_record(dataset, window, index)
        if any(actual.get(key) != value for key, value in expected.items()) or actual.get("actual_samples") != 22:
            raise ValueError("head-only sample history mismatch")
    for name in identity["frozen_parameter_names"]:
        torch.testing.assert_close(state["model"][name], parent["model"][name], atol=0, rtol=0)
    if count == 0:
        if not _state_equal(state["model"], parent["model"]):
            raise ValueError("H0 model does not exactly inherit G10")
        if any(_tensor_sha256(state["optimizer"]["state"][row["head_optimizer_slot"]]["momentum_buffer"])
               != row["momentum_sha256"] for row in identity["optimizer_name_mapping"]):
            raise ValueError("H0 optimizer momentum does not exactly inherit named G10 slots")
        streams = ("python", "numpy", "torch", "cuda") if candidate else ("python", "numpy", "torch")
        if any(not _state_equal(state["rng_state"][name], parent["rng_state"][name]) for name in streams):
            raise ValueError("H0 RNG does not exactly inherit G10")
    if candidate and not state["rng_state"]["cuda"]:
        raise ValueError("candidate lost parent CUDA RNG stream")


def restore(path, model, optimizer, identity, protocol, ancestry, parent, dataset, window, *, candidate):
    state = torch.load(path, map_location="cpu", weights_only=False)
    validate_state(state, identity, protocol, ancestry, parent, dataset, window, candidate=candidate)
    model.load_state_dict(state["model"], strict=True)
    optimizer.load_state_dict(state["optimizer"])
    restore_rng(state["rng_state"])
    return state


def cpu_check():
    CHECK_DIR.mkdir(exist_ok=False)
    if os.environ.get("CUDA_VISIBLE_DEVICES") != "-1" or torch.cuda.is_available() or torch.cuda.is_initialized():
        raise RuntimeError("CPU gate requires CUDA_VISIBLE_DEVICES=-1")
    torch.set_num_threads(2)
    torch.use_deterministic_algorithms(True)
    dataset, window, folded, identity, protocol, ancestry, parent = prepare()
    sources = CHECK_DIR / "sources"
    sources.mkdir()
    for index, (relative, digest) in enumerate(identity["source_sha256"].items()):
        target = sources / f"{index}_{Path(relative).name}"
        shutil.copyfile(base.PROJECT / relative, target)
        if sha256(target) != digest:
            raise ValueError("CPU gate source snapshot differs")
    device = torch.device("cpu")
    model, optimizer = model_and_optimizer(folded, device, parent, identity)
    restore_rng(parent["rng_state"])
    history = [update_once(model, optimizer, dataset, window, 0, device)]
    saved = copy.deepcopy(checkpoint(model, optimizer, identity, protocol, ancestry, history, candidate=False))
    validate_state(saved, identity, protocol, ancestry, parent, dataset, window, candidate=False)
    path = CHECK_DIR / "resume_check/update_H1.pt"
    base.commit(path, saved)
    history.append(update_once(model, optimizer, dataset, window, 1, device))
    continuous = copy.deepcopy(checkpoint(model, optimizer, identity, protocol, ancestry, history, candidate=False))
    validate_state(continuous, identity, protocol, ancestry, parent, dataset, window, candidate=False)
    resumed_model, resumed_optimizer = model_and_optimizer(folded, device, parent, identity)
    resumed_state = restore(path, resumed_model, resumed_optimizer, identity, protocol,
                            ancestry, parent, dataset, window, candidate=False)
    resumed_history = copy.deepcopy(resumed_state["sample_history"])
    resumed_history.append(update_once(resumed_model, resumed_optimizer, dataset, window, 1, device))
    resumed = checkpoint(resumed_model, resumed_optimizer, identity, protocol,
                         ancestry, resumed_history, candidate=False)
    validate_state(resumed, identity, protocol, ancestry, parent, dataset, window, candidate=False)
    for field in ("model", "optimizer", "rng_state", "local_trained_steps", "global_qat_updates"):
        if not _state_equal(continuous[field], resumed[field]):
            raise AssertionError(f"continuous versus resumed mismatch: {field}")
    for left, right in zip(continuous["sample_history"], resumed["sample_history"], strict=True):
        if ({key: value for key, value in left.items() if key != "seconds"}
                != {key: value for key, value in right.items() if key != "seconds"}):
            raise AssertionError("continuous versus resumed sample history mismatch")
    negatives = []
    for name, mutation in (
            ("ancestry", lambda value: value.update(ancestry={})),
            ("cursor", lambda value: value.update(next_local_update=0)),
            ("frozen", lambda value: value["model"][identity["frozen_parameter_names"][0]].add_(1)),
            ("optimizer_name", lambda value: value.update(optimizer_name_map=[]))):
        bad = copy.deepcopy(saved)
        mutation(bad)
        try:
            validate_state(bad, identity, protocol, ancestry, parent, dataset, window, candidate=False)
        except (ValueError, AssertionError):
            negatives.append(name)
        else:
            raise AssertionError(f"negative head-only state accepted: {name}")
    save(CHECK_DIR / "CPU_resume_check.json", dict(passed=True, identity=identity, protocol=protocol,
        ancestry_receipt=dict(parent_checkpoint_sha256=PARENT_SHA256,
                              parent_identity_sha256=identity["parent_identity_sha256"],
                              parent_sample_history_sha256=identity["parent_sample_history_sha256"]),
        optimizer_mapping_sha256=identity["optimizer_name_mapping_sha256"],
        trainable_parameter_tensors=42, frozen_parameter_tensors=92,
        continuous_local_updates=[1, 2], resumed_local_update=2,
        resumed_second_update_exact=True, negative_cases=negatives,
        cpu_threads=torch.get_num_threads(), pytorch_nvml_based_cuda_check="1",
        optimizer_updates_published=0, candidate_training_started=False,
        cuda_initialized=torch.cuda.is_initialized()))
    print(json.dumps(dict(event="CPU_head_only_resume_check_passed",
                          parent_checkpoint_sha256=PARENT_SHA256)), flush=True)


def worker(args):
    torch.set_num_threads(2)
    dataset, window, folded, identity, protocol, ancestry, parent = prepare()
    gate = base.read(CHECK_DIR / "CPU_resume_check.json")
    if (gate.get("passed") is not True or gate.get("identity") != identity
            or gate.get("protocol") != protocol or gate.get("trainable_parameter_tensors") != 42):
        raise ValueError("head-only CPU gate missing or stale")
    print(json.dumps(dict(event="preflight_ready", trainer_pid=os.getpid(),
        dataset_sha256=identity["dataset_sha256"], dataset_content_sha256=identity["dataset_content_sha256"],
        identity_sha256=protocol_hash(identity), resume=str(args.resume.resolve()) if args.resume else None)), flush=True)
    if not args.supervised_start or input().strip() != "GO":
        raise RuntimeError("owned watchdog GO required")
    torch.use_deterministic_algorithms(True)
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    device = torch.device("cuda")
    actual_uuid = str(getattr(torch.cuda.get_device_properties(device), "uuid", "")).removeprefix("GPU-")
    if actual_uuid.lower() != base.GPU.removeprefix("GPU-").lower():
        raise ValueError("CUDA GPU UUID differs from watchdog")
    model, optimizer = model_and_optimizer(folded, device, parent, identity)
    if args.resume:
        if args.resume.resolve().parent != RUN.resolve():
            raise ValueError("resume must belong to this fixed head-only run")
        state = restore(args.resume, model, optimizer, identity, protocol,
                        ancestry, parent, dataset, window, candidate=True)
        history = copy.deepcopy(state["sample_history"])
    else:
        parent_rng = copy.deepcopy(parent["rng_state"])
        previous_out = continuation.OUT
        continuation.OUT = OUT
        try:
            continuation.gpu_check(model, dataset, folded, parent, identity)
        finally:
            continuation.OUT = previous_out
        restore_rng(parent_rng)
        RUN.mkdir(exist_ok=False)
        history = []
        base.commit(RUN / "update_H0.pt", checkpoint(
            model, optimizer, identity, protocol, ancestry, history, candidate=True))
    for local_update in range(len(history), UPDATES):
        record = update_once(model, optimizer, dataset, window, local_update, device, args.pause_request)
        if record is None:
            print(json.dumps(dict(event="paused_qat", local_trained_steps=len(history),
                                  checkpoint=str(RUN / f"update_H{len(history)}.pt"),
                                  partial_update_discarded=True)), flush=True)
            return
        history.append(record)
        state = checkpoint(model, optimizer, identity, protocol, ancestry, history, candidate=True)
        validate_state(state, identity, protocol, ancestry, parent, dataset, window, candidate=True)
        path = RUN / f"update_H{len(history)}.pt"
        digest = base.commit(path, state)
        temporary = RUN / "last.pt.tmp"
        shutil.copyfile(path, temporary)
        with temporary.open("rb+") as stream:
            os.fsync(stream.fileno())
        os.replace(temporary, RUN / "last.pt")
        print(json.dumps(dict(event="qat_head_update_saved", local_trained_steps=len(history),
                              global_qat_updates=PRIOR_GLOBAL_UPDATES + len(history),
                              checkpoint=str(path), checkpoint_sha256=digest, **record)), flush=True)
    cpu = QATExactModel.from_package(base.BASE / "package", folded, base.BASE / "quantization.json")
    cpu.load_state_dict({name: value.cpu() for name, value in model.state_dict().items()}, strict=True)
    exported = write_package(OUT / "package", cpu.graph, cpu.integer_parameters(), cpu.scales,
        dict(purpose="QAT_HEAD_ONLY_G5_DEVELOPMENT_CANDIDATE",
             checkpoint_sha256=sha256(RUN / "last.pt"), source_checkpoint_sha256=base.CHECKPOINT_HASH,
             parent_checkpoint_sha256=PARENT_SHA256, trained_steps=UPDATES,
             local_head_only_updates=UPDATES, global_qat_updates=GLOBAL_UPDATES,
             identity=identity, trainable_parameter_tensors=42, frozen_parameter_tensors=92,
             qat_exact_fixed_weight_scales=True))
    integer, _ = load_package(OUT / "package")
    sample = dataset[0][0]
    with torch.no_grad():
        _, trace = cpu(sample.unsqueeze(0), capture=True)
    if len(trace) != 181:
        raise AssertionError("deployment trace count changed")
    _, _, exact = integer.forward(centered(sample), capture=True)
    values = 0
    for name, value in trace.items():
        scale = 1 / 256 if name.endswith(":pre") else cpu.scales[name]
        recovered = torch.round(value / scale)[0].permute(1, 2, 0).numpy()
        np.testing.assert_array_equal(recovered, exact[name])
        values += recovered.size
    save(OUT / "export_parity.json", dict(passed=True, trace_tensors=181, values=values,
        payload_sha256=exported["payload_sha256"], checkpoint_sha256=sha256(RUN / "last.pt"),
        trained_steps=UPDATES, local_head_only_updates=UPDATES, global_qat_updates=GLOBAL_UPDATES,
        parent_checkpoint_sha256=PARENT_SHA256, identity=identity, image=dataset[0][2], formal_acceptance=False))
    print(json.dumps(dict(event="completed_qat_head_only_G5", local_trained_steps=UPDATES,
        global_qat_updates=GLOBAL_UPDATES, checkpoint=str(RUN / "last.pt"),
        checkpoint_sha256=sha256(RUN / "last.pt"))), flush=True)


def execute():
    if RUN.exists() or (OUT / "execution").exists():
        raise FileExistsError("head-only trial already exists; no automatic retry")
    dataset, window, _folded, identity, protocol, ancestry, parent = prepare()
    gate = base.read(CHECK_DIR / "CPU_resume_check.json")
    if gate.get("passed") is not True or gate.get("identity") != identity or gate.get("protocol") != protocol:
        raise ValueError("head-only CPU gate missing or stale")
    folder = OUT / "execution"
    folder.mkdir()
    (folder / "sources").mkdir()
    for index, (relative, digest) in enumerate(identity["source_sha256"].items()):
        target = folder / "sources" / f"{index}_{Path(relative).name}"
        shutil.copyfile(base.PROJECT / relative, target)
        if sha256(target) != digest:
            raise ValueError("source snapshot differs")
    command = [sys._base_executable, "-u", "-B", "-m", WORKER_MODULE, "worker"]
    ancestry_receipt = dict(parent_checkpoint_sha256=PARENT_SHA256,
        parent_identity_sha256=identity["parent_identity_sha256"],
        parent_sample_history_sha256=identity["parent_sample_history_sha256"],
        parent_rng_streams=list(ancestry["parent_rng_state"]))
    save(OUT / "training_contract.json", dict(command=command, identity=identity, protocol=protocol,
        ancestry_receipt=ancestry_receipt, planned_local_updates=UPDATES,
        prior_global_qat_updates=PRIOR_GLOBAL_UPDATES, global_qat_updates_after_segment=GLOBAL_UPDATES,
        overall_qat_budget_cap=100, actual_samples_per_update=22, temperature_stop_c=75,
        hard_segment_seconds=1800, additional_ram_hard_threshold=False,
        automatic_retry=False, automatic_continuation=False, formal_acceptance=False))

    def complete(event):
        if event.get("event") == "paused_qat":
            state = torch.load(event["checkpoint"], map_location="cpu", weights_only=False)
            validate_state(state, identity, protocol, ancestry, parent, dataset, window, candidate=True)
            return dict(status="paused_no_auto_resume", saved_local_updates=state["local_trained_steps"])
        if event.get("event") != "completed_qat_head_only_G5" or event.get("local_trained_steps") != UPDATES:
            raise ValueError("missing complete head-only event")
        for count in range(UPDATES + 1):
            state = torch.load(RUN / f"update_H{count}.pt", map_location="cpu", weights_only=False)
            validate_state(state, identity, protocol, ancestry, parent, dataset, window, candidate=True)
        parity = base.read(OUT / "export_parity.json")
        final_digest = sha256(RUN / f"update_H{UPDATES}.pt")
        if (sha256(RUN / "last.pt") != final_digest or final_digest != event["checkpoint_sha256"]
                or parity.get("passed") is not True or parity.get("trace_tensors") != 181
                or parity.get("local_head_only_updates") != UPDATES):
            raise ValueError("final head-only export/commit differs")
        return dict(status="completed_qat_head_only_G5", checkpoint_sha256=final_digest,
                    saved_local_updates=UPDATES, global_qat_updates=GLOBAL_UPDATES,
                    all_saved_nonhead_parameter_tensors_unchanged=92)

    options = SimpleNamespace(receipt=folder / "segment.json", output=RUN,
                              gpu_uuid=base.GPU, preflight_timeout_seconds=180)
    started = time.perf_counter()
    result = base.run_protected(command, options, expected_ready=dict(
        dataset_sha256=identity["dataset_sha256"], dataset_content_sha256=identity["dataset_content_sha256"],
        identity_sha256=protocol_hash(identity), resume=None), completion_validator=complete)
    result.update(seconds=time.perf_counter() - started, formal_acceptance=False,
        parent_checkpoint_unchanged=sha256(PARENT) == PARENT_SHA256,
        sources_unchanged=all(sha256(base.PROJECT / name) == digest
                              for name, digest in identity["source_sha256"].items()))
    save(folder / "report.json", result)
    print(json.dumps(result), flush=True)
    if result["status"] != "completed_qat_head_only_G5":
        raise RuntimeError("head-only trial stopped; no automatic retry")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("check", "execute", "worker"))
    parser.add_argument("--pause-request", type=Path)
    parser.add_argument("--supervised-start", action="store_true")
    parser.add_argument("--resume", type=Path)
    args = parser.parse_args()
    if args.action == "check":
        OUT.mkdir(exist_ok=True)
        receipt = OUT / "cache_receipt.json"
        source_receipt = runtime.OUT / "cache_receipt.json"
        if not receipt.exists():
            shutil.copyfile(source_receipt, receipt)
        if sha256(receipt) != sha256(source_receipt):
            raise ValueError("runtime transition cache receipt changed")
        cpu_check()
    elif args.action == "execute":
        execute()
    else:
        worker(args)


if __name__ == "__main__":
    main()
