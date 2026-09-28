# Runtime reconnect suppression

This opt-in ESP32 API allows a radio-sharing component to temporarily stop WiFi
STA scanning and association attempts while leaving the WiFi driver initialized
and holding a chosen 2.4 GHz channel.

It is deliberately a mechanism, not a connectivity policy. The caller decides
when suppression starts, how long it remains active, when reconnect windows are
opened, and which channel is shared with ESP-NOW.

## Contract

- Code is compiled only after `enable_runtime_reconnect_suppression()` is called
  during component code generation.
- An established WiFi connection is never interrupted by a request.
- While disconnected, the first accepted request claims channels 1 through 14.
- Additional requesters may share the same channel.
- A different channel is rejected while a claim is active.
- Requests use a saturating count; releases cannot underflow.
- The ESP-IDF implementation stops an active scan, cancels association, and
  fixes the channel without stopping or deinitializing the WiFi driver.
- Releasing the final request starts a fresh WiFi scan.

The initial consumer is `espnow_net_protocol`, which will provide bounded hold
periods, reconnect windows, and per-device jitter in a separate change.

