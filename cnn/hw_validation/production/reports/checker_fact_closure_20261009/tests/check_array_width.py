"""复现并验证 VG097 对 unpacked array element 的位宽判定。"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path


SKILL = Path("C:/Users/lenovo/.codex/skills/readable-verilog-generator")
FIXTURES = {
    "unpacked_match": """\
module width_child (
    input wire [31:0] i_value
);
endmodule
module width_parent (
    input wire i_index
);
    reg [31:0] reg_values [0:1];
    width_child u_child (.i_value(reg_values[i_index]));
endmodule
""",
    "unpacked_mismatch": """\
module width_child (
    input wire [5:0] i_value
);
endmodule
module width_parent (
    input wire i_index
);
    reg [31:0] reg_values [0:1];
    width_child u_child (.i_value(reg_values[i_index]));
endmodule
""",
    "packed_bit_select": """\
module width_child (
    input wire i_value
);
endmodule
module width_parent (
    input wire i_index,
    input wire [31:0] i_value
);
    width_child u_child (.i_value(i_value[i_index]));
endmodule
""",
    "packed_bit_mismatch": """\
module width_child (
    input wire [5:0] i_value
);
endmodule
module width_parent (
    input wire i_index,
    input wire [31:0] i_value
);
    width_child u_child (.i_value(i_value[i_index]));
endmodule
""",
    "part_select": """\
module width_child (
    input wire [5:0] i_value
);
endmodule
module width_parent (
    input wire [31:0] i_value
);
    width_child u_child (.i_value(i_value[9:4]));
endmodule
""",
    "parameterized_unpacked": """\
module width_child #(
    parameter WIDTH = 6
) (
    input wire [WIDTH-1:0] i_value
);
endmodule
module width_parent #(
    parameter WIDTH = 6
) (
    input wire i_index
);
    reg [WIDTH-1:0] reg_values [0:1];
    width_child #(.WIDTH(WIDTH)) u_child (.i_value(reg_values[i_index]));
endmodule
""",
    "unknown_expression": """\
module width_child (
    input wire [31:0] i_value
);
endmodule
module width_parent (
    input wire [31:0] i_value
);
    width_child u_child (.i_value(i_value + 1'b1));
endmodule
""",
    "nested_select": """\
module width_child (
    input wire [5:0] i_value
);
endmodule
module width_parent (
    input wire i_index
);
    reg [31:0] reg_values [0:1];
    width_child u_child (.i_value(reg_values[i_index][5:0]));
endmodule
""",
    "multidimensional_single_select": """\
module width_child (
    input wire [31:0] i_value
);
endmodule
module width_parent (
    input wire i_index
);
    reg [31:0] reg_values [0:1][0:1];
    width_child u_child (.i_value(reg_values[i_index]));
endmodule
""",
    "unpacked_array_slice": """\
module width_child (
    input wire [3:0] i_value
);
endmodule
module width_parent ();
    reg [31:0] reg_values [0:7];
    width_child u_child (.i_value(reg_values[3:0]));
endmodule
""",
}
EXPECTED = {
    "unpacked_match": {"original": "failed", "overlay": "passed"},
    "unpacked_mismatch": {"original": "failed", "overlay": "failed"},
    "packed_bit_select": {"original": "passed", "overlay": "passed"},
    "packed_bit_mismatch": {"original": "failed", "overlay": "failed"},
    "part_select": {"original": "passed", "overlay": "passed"},
    "parameterized_unpacked": {"original": "failed", "overlay": "passed"},
    "unknown_expression": {"original": "inconclusive", "overlay": "inconclusive"},
    "nested_select": {"original": "inconclusive", "overlay": "inconclusive"},
    "multidimensional_single_select": {"original": "failed", "overlay": "inconclusive"},
    "unpacked_array_slice": {"original": "passed", "overlay": "inconclusive"},
}


def digest(path: Path) -> str:
    """返回标准文件 SHA256 或带路径 framing 的目录 fingerprint。"""

    if path.is_file():
        return hashlib.sha256(path.read_bytes()).hexdigest()
    hasher = hashlib.sha256()
    for item in sorted(item for item in path.rglob("*") if item.is_file()):
        hasher.update(item.relative_to(path).as_posix().encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(item.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def run_worker(args: argparse.Namespace) -> int:
    """在隔离解释器中加载原检查器或 overlay。"""

    sys.dont_write_bytecode = True
    paths = [str(SKILL)]
    if args.mode == "overlay":
        paths.insert(0, str(args.overlay.resolve()))
    sys.path[:0] = paths

    from scripts.python.quality.vg_instance_rules import _connection_port_width_match
    from scripts.python.quality.vg_semantic_facts import build_vg_facts
    import scripts.python.quality.vg_instance_rules as instance_rules
    import scripts.python.quality.vg_value_facts as value_facts

    evaluation = _connection_port_width_match(build_vg_facts(args.fixture))
    upstream_rules = sys.modules.get("scripts.python.quality._installed_vg_instance_rules")
    path_upstream = Path(upstream_rules.__file__) if upstream_rules is not None else None
    payload = {
        "mode": args.mode,
        "case": args.case,
        "actual": evaluation.status,
        "applicable": evaluation.applicable,
        "message": evaluation.message,
        "findings": [finding.to_dict() for finding in evaluation.findings],
        "imports": {
            "vg_instance_rules": str(Path(instance_rules.__file__).resolve()),
            "vg_instance_rules_sha256": digest(Path(instance_rules.__file__)),
            "vg_instance_rules_upstream": str(path_upstream.resolve()) if path_upstream else None,
            "vg_instance_rules_upstream_sha256": digest(path_upstream) if path_upstream else None,
            "vg_value_facts": str(Path(value_facts.__file__).resolve()),
            "vg_value_facts_sha256": digest(Path(value_facts.__file__)),
        },
        "fixture": str(args.fixture.resolve()),
        "fixture_digest_kind": "sha256" if args.fixture.is_file() else "directory_fingerprint_sha256",
        "fixture_digest": digest(args.fixture),
    }
    args.result.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


def run_matrix(args: argparse.Namespace) -> int:
    """生成固定 fixture，分别运行原检查器和 overlay。"""

    path_output = args.output.resolve()
    path_output.parent.mkdir(parents=True, exist_ok=True)
    path_fixtures = path_output.parent / f"{path_output.stem}_fixtures"
    path_fixtures.mkdir(exist_ok=True)
    path_workers = path_output.parent / f"{path_output.stem}_worker_results"
    path_workers.mkdir(exist_ok=True)
    rows = []
    for name, source in FIXTURES.items():
        path_fixture = path_fixtures / name
        path_fixture.mkdir(exist_ok=True)
        int_parent = source.index("module width_parent")
        (path_fixture / "width_child.v").write_text(
            source[:int_parent], encoding="utf-8", newline="\n"
        )
        (path_fixture / "width_parent.v").write_text(
            source[int_parent:], encoding="utf-8", newline="\n"
        )
        row = {
            "case": name,
            "fixture_directory_fingerprint_sha256": digest(path_fixture),
            "runs": {},
        }
        for mode in ("original", "overlay"):
            path_result = path_workers / f"{name}_{mode}.json"
            command = [
                sys.executable,
                "-B",
                "-X",
                "utf8",
                str(Path(__file__).resolve()),
                "--worker",
                "--mode",
                mode,
                "--case",
                name,
                "--fixture",
                str(path_fixture),
                "--overlay",
                str(args.overlay.resolve()),
                "--result",
                str(path_result),
            ]
            environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
            completed = subprocess.run(
                command,
                cwd=Path(__file__).resolve().parent,
                capture_output=True,
                encoding="utf-8",
                env=environment,
                timeout=60,
                check=False,
            )
            if completed.returncode != 0 or not path_result.is_file():
                raise RuntimeError(
                    f"{name}/{mode} worker failed: {completed.returncode}\n"
                    f"{completed.stdout}{completed.stderr}"
                )
            actual = json.loads(path_result.read_text(encoding="utf-8"))
            actual["expected"] = EXPECTED[name][mode]
            actual["passed"] = actual["actual"] == actual["expected"]
            row["runs"][mode] = actual
        rows.append(row)

    payload = {
        "contract": "VG097 unpacked array element uses its packed element width",
        "overlay": str(args.overlay.resolve()),
        "skill": str(SKILL.resolve()),
        "new_parser_added": False,
        "shared_expression_width_changed": False,
        "file_digest": "sha256(file_bytes)",
        "fixture_directory_fingerprint": "sha256(relative_posix_path + NUL + file_bytes + NUL, sorted)",
        "cases": rows,
        "all_passed": all(run["passed"] for row in rows for run in row["runs"].values()),
    }
    path_output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"cases": len(rows), "all_passed": payload["all_passed"]}, ensure_ascii=False))
    return 0 if payload["all_passed"] else 1


def create_parser() -> argparse.ArgumentParser:
    """创建公开入口和隔离 worker 参数。"""

    parser = argparse.ArgumentParser()
    parser.add_argument("--overlay", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--mode", choices=("original", "overlay"), help=argparse.SUPPRESS)
    parser.add_argument("--case", help=argparse.SUPPRESS)
    parser.add_argument("--fixture", type=Path, help=argparse.SUPPRESS)
    parser.add_argument("--result", type=Path, help=argparse.SUPPRESS)
    return parser


def main() -> int:
    """运行 VG097 位宽事实回归。"""

    args = create_parser().parse_args()
    if args.worker:
        if not all((args.mode, args.case, args.fixture, args.result)):
            raise SystemExit("worker arguments are incomplete")
        return run_worker(args)
    if args.output is None:
        raise SystemExit("--output is required")
    return run_matrix(args)


if __name__ == "__main__":
    raise SystemExit(main())
