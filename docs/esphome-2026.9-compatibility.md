# ESPHome 2026.9.1 compatibility backport

Failure: captive_portal.cpp includes esphome/components/wifi/scan_list.h, absent from this override.

Backported from upstream tag 2026.9.1:
- scan_list.h, unmodified.
- WiFiScanResult::ssid_equals(const WiFiScanResult &) const, comparing CompactString SSIDs.

Upstream: https://github.com/esphome/esphome/tree/2026.9.1/esphome/components/wifi

Header SHA-256: 031f47d6c8ee255b0fd75dc2785f199e777d1062a2a144260a10bfb69ef0238d

No configuration or arbitration changes. Firmware compilation and device validation remain pending.
