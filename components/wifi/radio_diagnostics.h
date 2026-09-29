#pragma once

#include <cstddef>
#include <cstdint>
#include <type_traits>

namespace esphome {
namespace wifi {

// Plain bounded storage. Written/read only on the main loop, never in IDF callbacks.
template<typename T, size_t N> struct RadioDiagnosticRing {
  T items[N]{};
  uint16_t next{0};
  uint16_t count{0};
  uint32_t total{0};
  void push(const T &item) {
    items[next] = item;
    next = (next + 1) % N;
    if (count < N) ++count;
    ++total;
  }
  bool valid() const { return next < N && count <= N; }
  const T &at(size_t index) const { return items[(next + N - count + index) % N]; }
};

enum class RadioDiagnosticEventKind : uint16_t {
  WIFI_STOP_CALL = 1, WIFI_STOP_RESULT, WIFI_START_RESULT, WIFI_MODE_RESULT,
  STA_START, STA_STOP, ASSOCIATED, DISCONNECTED, GOT_IP, LOST_IP,
  SCAN_START_RESULT, SCAN_STOP_RESULT, DISCONNECT_RESULT, SET_CHANNEL_RESULT,
  ESPNOW_INIT_RESULT, ESPNOW_DEINIT_CALL, ESPNOW_DEINIT_RESULT,
  STATE_CHANGE,
};

inline const char *radio_diagnostic_event_name(RadioDiagnosticEventKind kind) {
  using E = RadioDiagnosticEventKind;
  switch (kind) {
    case E::WIFI_STOP_CALL: return "wifi_stop_call";
    case E::WIFI_STOP_RESULT: return "wifi_stop_result";
    case E::WIFI_START_RESULT: return "wifi_start_result";
    case E::WIFI_MODE_RESULT: return "wifi_mode_result";
    case E::STA_START: return "sta_start";
    case E::STA_STOP: return "sta_stop";
    case E::ASSOCIATED: return "associated";
    case E::DISCONNECTED: return "disconnected";
    case E::GOT_IP: return "got_ip";
    case E::LOST_IP: return "lost_ip";
    case E::SCAN_START_RESULT: return "scan_start_result";
    case E::SCAN_STOP_RESULT: return "scan_stop_result";
    case E::DISCONNECT_RESULT: return "disconnect_result";
    case E::SET_CHANNEL_RESULT: return "set_channel_result";
    case E::ESPNOW_INIT_RESULT: return "espnow_init_result";
    case E::ESPNOW_DEINIT_CALL: return "espnow_deinit_call";
    case E::ESPNOW_DEINIT_RESULT: return "espnow_deinit_result";
    case E::STATE_CHANGE: return "state_change_flags_arb";
  }
  return "unknown";
}

struct RadioDiagnosticEvent {
  uint32_t uptime_ms{0};
  int32_t result{0};
  RadioDiagnosticEventKind kind{};
  uint16_t detail{0};  // channel, WiFi mode, or IDF disconnect reason
};
using RadioDiagnosticEvents = RadioDiagnosticRing<RadioDiagnosticEvent, 64>;

struct RadioDiagnosticWifiState {
  uint8_t state{0};
  bool driver_started{false};  // WiFi component bookkeeping, not an RF measurement
  bool sta_started{false};    // last processed STA_START/STA_STOP event
  bool connecting{false};
  uint16_t last_disconnect_reason{0};
  uint32_t stop_calls{0};
};

static_assert(std::is_trivially_copyable<RadioDiagnosticEvents>::value, "Persisted diagnostic layout");
}  // namespace wifi
}  // namespace esphome
