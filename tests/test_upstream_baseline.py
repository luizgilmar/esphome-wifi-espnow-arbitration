from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "components" / "wifi"
MANIFEST = ROOT / "docs" / "upstream-baseline.sha256"


def _manifest() -> dict[str, str]:
    entries: dict[str, str] = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        if not line:
            continue
        digest, relative_path = line.split(maxsplit=1)
        entries[relative_path] = digest
    return entries


def test_external_component_layout_is_complete() -> None:
    expected = {
        "__init__.py",
        "automation.h",
        "wifi_component.cpp",
        "wifi_component.h",
        "wifi_component_esp_idf.cpp",
        "wifi_component_esp8266.cpp",
        "wifi_component_libretiny.cpp",
        "wifi_component_pico_w.cpp",
        "wpa2_eap.py",
    }
    actual = {path.name for path in COMPONENT.iterdir() if path.is_file()}
    assert actual == expected


def test_baseline_matches_esphome_2026_7_3_archive() -> None:
    expected_modified = {
        "components/wifi/__init__.py",
        "components/wifi/wifi_component.cpp",
        "components/wifi/wifi_component.h",
        "components/wifi/wifi_component_esp_idf.cpp",
    }
    for relative_path, expected_digest in _manifest().items():
        if relative_path in expected_modified:
            continue
        payload = (ROOT / relative_path).read_bytes()
        actual_digest = hashlib.sha256(payload).hexdigest()
        assert actual_digest == expected_digest, relative_path


def test_python_cache_is_not_distributed() -> None:
    assert not list(COMPONENT.rglob("__pycache__"))
    assert not list(COMPONENT.rglob("*.pyc"))
