from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WIFI = ROOT / "components" / "wifi"


def read(name: str) -> str:
    return (WIFI / name).read_text(encoding="utf-8")


def test_codegen_feature_is_explicit_and_opt_in() -> None:
    schema = read("__init__.py")
    assert 'RUNTIME_RECONNECT_SUPPRESSION_KEY = "wifi_runtime_reconnect_suppression"' in schema
    assert "def enable_runtime_reconnect_suppression()" in schema
    assert 'cg.add_define("USE_WIFI_RUNTIME_RECONNECT_SUPPRESSION")' in schema


def test_public_api_is_bounded_and_channel_aware() -> None:
    header = read("wifi_component.h")
    source = read("wifi_component.cpp")
    assert "bool request_reconnect_suppression(uint8_t channel)" in header
    assert "void release_reconnect_suppression()" in header
    assert "std::atomic<uint16_t> reconnect_suppression_state_{0}" in header
    assert "channel < 1 || channel > 14" in source
    assert "claimed_channel != channel" in source
    assert "std::numeric_limits<uint8_t>::max()" in source


def test_suppression_preserves_driver_and_holds_channel() -> None:
    source = read("wifi_component.cpp")
    idf = read("wifi_component_esp_idf.cpp")
    block_start = idf.index("bool WiFiComponent::wifi_enter_reconnect_suppression_")
    block_end = idf.index("\n}\n#endif", block_start)
    block = idf[block_start:block_end]
    assert "esp_wifi_scan_stop()" in block
    assert "esp_wifi_disconnect()" in block
    assert "esp_wifi_set_channel(channel, WIFI_SECOND_CHAN_NONE)" in block
    assert "esp_wifi_stop" not in block
    assert "wifi_mode_(false" not in block
    assert "WIFI_COMPONENT_STATE_RECONNECT_SUPPRESSED" in source
    assert "this->start_scanning();" in source

