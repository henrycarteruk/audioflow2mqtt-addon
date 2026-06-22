# Audioflow Speaker Selector

Local control of Audioflow speaker switches over MQTT, with Home Assistant MQTT
discovery. The add-on finds your Audioflow devices automatically on the local network
via UDP discovery, or you can set their IP addresses.

## Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `mqtt_host` | _(empty)_ | IP address or hostname of the MQTT broker. Leave empty to use the broker provided by Home Assistant. |
| `mqtt_port` | `1883` | Port the MQTT broker listens on. Ignored when using the Home Assistant broker. |
| `mqtt_user` | _(empty)_ | Username for the MQTT broker. Leave empty when using the Home Assistant broker. |
| `mqtt_pass` | _(empty)_ | Password for the MQTT broker. Leave empty when using the Home Assistant broker. |
| `qos` | `1` | MQTT Quality of Service level (`0`–`2`) for published messages. |
| `base_topic` | `audioflow2mqtt` | Topic prefix used for all published and subscribed topics. |
| `devices` | _(empty)_ | IP addresses of your Audioflow devices. Leave empty to discover them automatically. |
| `log_level` | `info` | Minimum log level: `debug`, `info`, `warning`, or `error`. |

When `mqtt_host` is left empty, the broker host, port, username, and password are taken
automatically from the Home Assistant MQTT service. Home Assistant MQTT discovery is
always enabled.

For reliability, give each Audioflow device a static IP (e.g. a DHCP reservation) and
set `devices`, rather than relying on UDP discovery. UDP discovery only works when the
device is on the same subnet as Home Assistant.

## What you get in Home Assistant

A device is created for each Audioflow switch, with:

- Switch entities for each zone
- Buttons to turn all zones on and off
- Sensors for SSID, Wi-Fi channel, and RSSI (signal strength)

## MQTT topics

All topics are prefixed with your `base_topic` (default `audioflow2mqtt`). The examples
use the default base topic and the serial number `0123456789` (on the sticker on the
bottom of the device). Zones are numbered A = 1, B = 2, and so on.

### Commands you send

| Command topic | Payload | Effect |
|---------------|---------|--------|
| `audioflow2mqtt/0123456789/set_zone_state/<zone>` | `on`, `off`, `toggle` | Turn one zone on/off, or toggle it |
| `audioflow2mqtt/0123456789/set_zone_state` | `on`, `off` | Turn all zones on/off (no zone number) |
| `audioflow2mqtt/0123456789/set_zone_enable/<zone>` | `1`, `0` | Enable (`1`) or disable (`0`) one zone |
| `audioflow2mqtt/discover` | _(any)_ | Trigger a fresh UDP discovery sweep |

### Topics the add-on publishes

- `audioflow2mqtt/0123456789/zone_state/<zone>` — `on` or `off`
- `audioflow2mqtt/0123456789/zone_enabled/<zone>` — `1` or `0`
- `audioflow2mqtt/0123456789/network_info/{ssid,channel,rssi}` — network info, polled periodically
- `audioflow2mqtt/status` — `online`/`offline` for the add-on (retained)
- `audioflow2mqtt/0123456789/status` — `online`/`offline` per device (retained)

The device does not report a new state after a command, so the add-on re-reads the
affected zone(s) and republishes.

## Notes

A single instance handles multiple Audioflow devices — every topic is namespaced by the
device serial number, so they do not collide.
