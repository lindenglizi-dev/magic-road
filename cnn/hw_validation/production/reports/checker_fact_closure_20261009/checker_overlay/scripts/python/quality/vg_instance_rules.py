"""Project-local VG097 fix for unpacked array element widths."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

from . import vg_value_facts


class _DeclarationWidths(dict[str, int | None]):
    """Carry formatter declaration shape beside the existing width mapping."""

    def __init__(
        self,
        widths: dict[str, int | None],
        unpacked_names: frozenset[str],
        single_unpacked_names: frozenset[str],
    ) -> None:
        super().__init__(widths)
        self.unpacked_names = unpacked_names
        self.single_unpacked_names = single_unpacked_names


def _load_upstream_module():
    """Load the installed implementation so unrelated VG097 behavior stays upstream."""

    path_current = Path(__file__).resolve()
    package = sys.modules[__package__]
    for path_entry in package.__path__:
        path_candidate = (Path(path_entry) / path_current.name).resolve()
        if path_candidate == path_current or not path_candidate.is_file():
            continue
        str_name = f"{__package__}._installed_vg_instance_rules"
        spec = importlib.util.spec_from_file_location(str_name, path_candidate)
        if spec is None or spec.loader is None:
            break
        module = importlib.util.module_from_spec(spec)
        sys.modules[str_name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError("installed vg_instance_rules.py was not found")


def _module_widths(
    dict_module: dict[str, object],
    parameter_overrides: dict[str, int] | None = None,
) -> _DeclarationWidths:
    """Reuse shared widths and retain formatter-provided unpacked dimensions."""

    widths = vg_value_facts.module_widths(dict_module, parameter_overrides)
    unpacked: set[str] = set()
    single: set[str] = set()
    for collection in ("ports", "decls"):
        for item in dict_module.get(collection, []) or []:
            text = str(item.get("unpacked") or "").strip()
            name = str(item.get("name") or "")
            if not text or not name:
                continue
            unpacked.add(name)
            if re.fullmatch(r"\[[^\[\]]+\]", text):
                single.add(name)
    return _DeclarationWidths(widths, frozenset(unpacked), frozenset(single))


def _expression_width(
    str_expression: str,
    dict_widths: dict[str, int | None],
) -> int | None:
    """Resolve only a one-dimensional unpacked element before upstream logic."""

    value = vg_value_facts.strip_outer_parentheses(str_expression.strip())
    match = re.fullmatch(r"([A-Za-z_]\w*)\s*\[\s*([^\[\]]+?)\s*\]", value)
    if match is not None and isinstance(dict_widths, _DeclarationWidths):
        name, selector = match.groups()
        if name in dict_widths.unpacked_names:
            if name in dict_widths.single_unpacked_names and ":" not in selector:
                return dict_widths.get(name)
            return None
    return vg_value_facts.expression_width(str_expression, dict_widths)


_upstream = _load_upstream_module()
_upstream.module_widths = _module_widths
_upstream.expression_width = _expression_width

# vg_control_rules imports only this public rule emitter. The loaded private copy
# keeps every other VG097 branch byte-for-byte upstream.
_connection_port_width_match = _upstream._connection_port_width_match
