"""Narrow parser adaptations layered on the installed formatter parser."""

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
        str_name = f"{__package__}._installed_parse_mixin"
        spec = importlib.util.spec_from_file_location(str_name, path_candidate)
        if spec is None or spec.loader is None:
            break
        module = importlib.util.module_from_spec(spec)
        sys.modules[str_name] = module
        spec.loader.exec_module(module)
        return module
    raise ImportError("installed formatter parse_mixin.py was not found")


_upstream = _load_upstream_module()


class ParseMixin(_upstream.ParseMixin):
    """Accept two legal source shapes before delegating to the original parser."""

    def _parse_module(self, source: str):
        """Normalize a bare zero-port module header to its equivalent ``()`` form."""

        str_normalized = re.sub(
            r"(?m)^(?P<prefix>[ \t]*module[ \t]+[A-Za-z_]\w*[ \t]*);",
            r"\g<prefix>();",
            source,
            count=1,
        )
        return super()._parse_module(str_normalized)

    def _split_always_header(self, text: str) -> tuple[str, str]:
        """Split a simple periodic ``always #value`` control or use the original path."""

        obj_delay = re.fullmatch(
            r"[ \t]*always[ \t]+#[ \t]*(?P<delay>(?:\d+(?:\.\d+)?|[A-Za-z_]\w*))"
            r"(?:[ \t]+(?P<body>.*))?[ \t]*",
            text,
        )
        if obj_delay is None:
            return super()._split_always_header(text)
        str_body = (obj_delay.group("body") or "").strip()
        return f"always #{obj_delay.group('delay')}", str_body
