"""Execute the real configuration validator without installing ESPHome."""
import ast
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1] / "components/wifi/__init__.py"

def validator():
    tree = ast.parse(SOURCE.read_text(encoding="utf-8"))
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_validate_fixed_channel")
    namespace = {"cv": SimpleNamespace(Invalid=ValueError)}
    exec(compile(ast.Module(body=[fn], type_ignores=[]), str(SOURCE), "exec"), namespace)
    return namespace[fn.name]

def test_legacy_configuration_is_unchanged():
    config = {"enable_rrm": True, "networks": [{"channel": 6}]}
    assert validator()(config) is config

def test_retry_interval_accepts_bounds_and_bench_value():
    for milliseconds in (10000, 120000, 300000):
        config = {"fixed_channel": 1, "fixed_channel_retry_interval": SimpleNamespace(total_milliseconds=milliseconds)}
        assert validator()(config) is config

def test_retry_interval_rejects_out_of_bounds():
    for milliseconds in (0, 9999, 300001):
        try:
            validator()({"fixed_channel": 1, "fixed_channel_retry_interval": SimpleNamespace(total_milliseconds=milliseconds)})
        except ValueError:
            continue
        raise AssertionError(f"Accepted out-of-bounds retry: {milliseconds}")

def test_retry_interval_requires_fixed_channel():
    try:
        validator()({"fixed_channel_retry_interval": SimpleNamespace(total_milliseconds=120000)})
    except ValueError:
        return
    raise AssertionError("Accepted retry interval without fixed channel")

def test_fixed_channel_accepts_saved_credentials_without_channel():
    config = {"fixed_channel": 1, "networks": [{"ssid": "lab"}], "ap": {"channel": 1}}
    assert validator()(config) is config

def test_fixed_channel_accepts_multiple_aps_on_one_channel():
    config = {"fixed_channel": 1, "networks": [{"channel": 1}, {"channel": 1}]}
    assert validator()(config) is config

def test_fixed_channel_rejects_conflicting_sources():
    for addition in ({"enable_btm": True}, {"enable_rrm": True},
                     {"networks": [{"channel": 6}]}, {"ap": {"channel": 11}}):
        try:
            validator()({"fixed_channel": 1, **addition})
        except ValueError:
            continue
        raise AssertionError(f"Accepted conflicting config: {addition}")
