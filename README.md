# ESPHome WiFi ESP-NOW Arbitration

Temporary external override of ESPHome's built-in `wifi` component, based on
ESPHome 2026.7.3.

The repository exists to validate a minimal and generic WiFi/ESP-NOW radio
arbitration API before proposing the change upstream. The baseline commit must
remain behaviorally identical to the upstream component.

## Baseline

- ESPHome version: `2026.7.3`
- Component: `esphome/components/wifi`
- Baseline source archive: `esphome-wifi-2026.7.3.zip`
- Baseline source hashes: `docs/upstream-baseline.sha256`

## ESPHome usage

Pin a tag or commit. Do not consume the development branch directly in
production devices.

```yaml
external_components:
  - source:
      type: git
      url: https://github.com/luizgilmar/esphome-wifi-espnow-arbitration
      ref: v2026.7.3-espnow.1
    components:
      - wifi
```

The component keeps the name `wifi` intentionally: it replaces the built-in
ESPHome component during code generation.

## Development policy

1. Preserve an immutable baseline commit containing only the 2026.7.3 source.
2. Keep arbitration generic and opt-in.
3. Do not embed device, room, MQTT, or application-specific policy in `wifi`.
4. Keep the radio driver running while reconnect attempts are suppressed.
5. Compile at least one ESP32 and one ESP32-S3 configuration before tagging.
6. Pin every consumer to a reviewed tag or commit.

## Tests

```powershell
python -m pytest -q
```

The baseline test verifies repository layout and the exact upstream file
hashes. It will intentionally need revision in the first functional commit.

