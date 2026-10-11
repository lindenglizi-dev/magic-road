"""Narrow rendering adaptation layered on the installed syntax helpers."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _load_upstream_module():
    """Load the installed implementation under a private sibling name."""

    path_current = Path(__file__).resolve()
    package = sys.modules[__package__]
    for path_entry in package.__path__:
        path_candidate = (Path(path_entry) / path_current.name).resolve()
        if path_candidate == path_current or not path_candidate.is_file():
            continue
        str_name = f"{__package__}._installed_syntax_utils"
        spec = importlib.util.spec_from_file_location(str_name, path_candidate)
        if spec is None or spec.loader is None:
            break
        module = importlib.util.module_from_spec(spec)
        sys.modules[str_name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError("installed formatter syntax_utils.py was not found")


_upstream = _load_upstream_module()


class SyntaxUtilsMixin(_upstream.SyntaxUtilsMixin):
    """Keep delay-control rendering lexically separated from ``begin``."""

    def _normalize_always_header(self, header: str) -> str:
        """Preserve the installed normalization and add one required delay spacer."""

        str_normalized = super()._normalize_always_header(header)
        if re.fullmatch(r"always[ \t]+#[ \t]*(?:\d+(?:\.\d+)?|[A-Za-z_]\w*)", str_normalized):
            return f"{str_normalized.rstrip()} "
        return str_normalized
