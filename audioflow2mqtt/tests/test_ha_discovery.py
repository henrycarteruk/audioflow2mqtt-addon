import json

from audioflow2mqtt.ha_discovery import (
    build_device_discovery,
    DiscoveryDevice,
    DiscoveryZone,
)


def _by_topic(messages, topic):
    return next(m for m in messages if m.topic == topic)


def _payload(message):
    return json.loads(message.payload)


DEVICE = DiscoveryDevice(
    serial="0123456789",
    name="Living Room",
    model="AF1",
    fw_version="1.2",
    zones=[DiscoveryZone(number=1, name="Kitchen", enabled=True)],
)


def test_disabled_zone_gets_disabled_suffix():
    device = DiscoveryDevice(
        serial="0123456789",
        name="Living Room",
        model="AF1",
        fw_version="1.2",
        zones=[
            DiscoveryZone(number=1, name="Kitchen", enabled=True),
            DiscoveryZone(number=2, name="Patio", enabled=False),
        ],
    )
    msgs = build_device_discovery("audioflow2mqtt", device)
    assert _payload(_by_topic(msgs, "homeassistant/switch/0123456789/1/config"))["name"] == "Kitchen speakers"
    assert _payload(_by_topic(msgs, "homeassistant/switch/0123456789/2/config"))["name"] == "Patio speakers (Disabled)"


def test_all_zones_buttons():
    msgs = build_device_discovery("audioflow2mqtt", DEVICE)
    on = _payload(_by_topic(msgs, "homeassistant/button/0123456789/all_zones_on/config"))
    off = _payload(_by_topic(msgs, "homeassistant/button/0123456789/all_zones_off/config"))
    assert on["command_topic"] == "audioflow2mqtt/0123456789/set_zone_state"
    assert on["payload_press"] == "on"
    assert on["unique_id"] == "0123456789_all_zones_on"
    assert off["payload_press"] == "off"
    assert off["unique_id"] == "0123456789_all_zones_off"


def test_network_info_sensors():
    msgs = build_device_discovery("audioflow2mqtt", DEVICE)
    ssid = _payload(_by_topic(msgs, "homeassistant/sensor/0123456789/ssid/config"))
    channel = _payload(_by_topic(msgs, "homeassistant/sensor/0123456789/channel/config"))
    rssi = _payload(_by_topic(msgs, "homeassistant/sensor/0123456789/rssi/config"))
    assert ssid["state_topic"] == "audioflow2mqtt/0123456789/network_info/ssid"
    assert ssid["name"] == "SSID"
    assert channel["name"] == "Wi-Fi channel"
    assert rssi["name"] == "RSSI"
    assert rssi["unique_id"] == "0123456789rssi"


def test_all_messages_share_availability_and_device():
    msgs = build_device_discovery("audioflow2mqtt", DEVICE)
    assert msgs
    for m in msgs:
        assert m.qos == 1
        assert m.retain is True
        payload = _payload(m)
        assert payload["availability"] == [
            {"topic": "audioflow2mqtt/status"},
            {"topic": "audioflow2mqtt/0123456789/status"},
        ]
        assert payload["device"] == {
            "name": "Living Room",
            "identifiers": "0123456789",
            "manufacturer": "Audioflow",
            "model": "AF1",
            "sw_version": "1.2",
        }
        assert payload["platform"] == "mqtt"


def test_switch_message_per_zone():
    msgs = build_device_discovery("audioflow2mqtt", DEVICE)
    sw = _payload(_by_topic(msgs, "homeassistant/switch/0123456789/1/config"))
    assert sw["command_topic"] == "audioflow2mqtt/0123456789/set_zone_state/1"
    assert sw["state_topic"] == "audioflow2mqtt/0123456789/zone_state/1"
    assert sw["unique_id"] == "01234567891"
    assert sw["name"] == "Kitchen speakers"
