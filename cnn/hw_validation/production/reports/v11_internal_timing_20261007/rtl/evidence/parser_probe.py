"""Expose the formatter exception chain for the frozen v10 runner."""
import sys
import traceback
import inspect
from pathlib import Path
from types import MethodType

sys.path.insert(0, r"C:\Users\lenovo\.codex\skills\readable-verilog-generator")

from scripts.python.quality.formatter_config import create_formatter_backend


DEFAULT_SOURCE = Path(
    r"E:\project\qiansai\anlogic_topic2_work\lab1_sc500_road_vision"
    r"\cnn\hw_validation\production\reports\v10_postprocess_overlap_20261007"
    r"\rtl\down2_overlap_tile_runner.v"
)
SOURCE = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_SOURCE

backend = create_formatter_backend(profile="formatter-normalize")
original_raise = backend._raise_control_error


def traced_raise(self, category, statement, suggestion):
    """Print the active parser fragment before preserving the real exception."""
    print(f"CATEGORY={category} STATEMENT={statement!r}")
    for frame in inspect.stack()[1:6]:
        local_lines = frame.frame.f_locals.get("lines")
        local_index = frame.frame.f_locals.get("int_index", frame.frame.f_locals.get("start"))
        if isinstance(local_lines, list) and isinstance(local_index, int):
            low = max(0, local_index - 4)
            high = min(len(local_lines), local_index + 5)
            print(f"FRAME={frame.function} INDEX={local_index} FRAGMENT={local_lines[low:high]!r}")
    original_raise(category, statement, suggestion)


backend._raise_control_error = MethodType(traced_raise, backend)

try:
    backend.format_text(
        SOURCE.read_text(encoding="utf-8"), SOURCE
    )
    print("FORMATTER_PASS")
except BaseException as error:
    traceback.print_exc()
    current = error
    while current is not None:
        print(f"{type(current).__name__}: {str(current)!r}")
        current = current.__cause__

