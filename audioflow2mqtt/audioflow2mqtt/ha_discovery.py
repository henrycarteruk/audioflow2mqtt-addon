"""Pure builders for Home Assistant MQTT discovery payloads.

Produces the retained `homeassistant/.../config` messages that make entities
appear automatically in Home Assistant. Payloads are serialized to JSON here and
returned as PublishMessage, so every discovery publish crosses the transport
seam as the same type as any other publish. No I/O.
"""
from __future__ import annotations

import json
from dataclasses import dataclass

from .mqtt import PublishMessage


@dataclass(frozen=True)
class DiscoveryZone:
    number: int
    name: str
    enabled: bool


@dataclass(frozen=True)
class DiscoveryDevice:
    serial: str
    name: str
    model: str
    fw_version: str
    zones: list[DiscoveryZone]


def build_device_discovery(base_topic: str, device: DiscoveryDevice) -> list[PublishMessage]:
    common = {
        "availability": [
            {"topic": f"{base_topic}/status"},
            {"topic": f"{base_topic}/{device.serial}/status"},
        ],
        "device": {
            "name": device.name,
            "identifiers": device.serial,
            "manufacturer": "Audioflow",
            "model": device.model,
            "sw_version": device.fw_version,
        },
        "platform": "mqtt",
    }
    messages: list[PublishMessage] = []
    for zone in device.zones:
        x = zone.number
        suffix = "" if zone.enabled else " (Disabled)"
        messages.append(_config(
            f"homeassistant/switch/{device.serial}/{x}/config",
            {
                **common,
                "name": f"{zone.name} speakers{suffix}",
                "command_topic": f"{base_topic}/{device.serial}/set_zone_state/{x}",
                "state_topic": f"{base_topic}/{device.serial}/zone_state/{x}",
                "payload_on": "on",
                "payload_off": "off",
                "unique_id": f"{device.serial}{x}",
            },
        ))

    for state in ("off", "on"):
        messages.append(_config(
            f"homeassistant/button/{device.serial}/all_zones_{state}/config",
            {
                **common,
                "name": f"Turn all zones {state}",
                "command_topic": f"{base_topic}/{device.serial}/set_zone_state",
                "payload_press": state,
                "unique_id": f"{device.serial}_all_zones_{state}",
                "icon": f"mdi:power-{state}",
            },
        ))

    for key, name, icon in _SENSORS:
        messages.append(_config(
            f"homeassistant/sensor/{device.serial}/{key}/config",
            {
                **common,
                "name": name,
                "state_topic": f"{base_topic}/{device.serial}/network_info/{key}",
                "icon": icon,
                "unique_id": f"{device.serial}{key}",
            },
        ))
    return messages


def _config(topic: str, payload: dict) -> PublishMessage:
    """A retained discovery config message with a JSON-serialized payload."""
    return PublishMessage(topic=topic, payload=json.dumps(payload), qos=1, retain=True)


_SENSORS = (
    ("ssid", "SSID", "mdi:access-point-network"),
    ("channel", "Wi-Fi channel", "mdi:access-point"),
    ("rssi", "RSSI", "mdi:signal"),
)
