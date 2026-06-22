# Changelog

All notable changes to this add-on are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and the add-on follows
[Semantic Versioning](https://semver.org/) — the `version` in `config.yaml` is the
release version Home Assistant uses to offer updates.

## 0.8.3

### Changed

- The add-on now stays running and retries discovery in the background instead of
  exiting when no devices are found at startup. A device that appears later — or a
  configured IP address that becomes reachable — is picked up without a restart.

## 0.8.2

### Added

- A description for every configuration option, shown as help text in the add-on
  configuration UI, including the QoS option.
- In-add-on documentation, shown in the add-on's Documentation tab.

## 0.8.1

### Fixed

- The add-on image now builds on Home Assistant. The base image is pinned directly
  in the Dockerfile, because the current Supervisor builder no longer reads
  `build.yaml` and otherwise substitutes an Alpine base that has no `pip`.
- The add-on now starts. Optional options (`mqtt_user`, `mqtt_pass`, `devices`)
  default to empty values instead of `null`, which the options validator rejected
  with "Missing required option".

## 0.8.0

- Rewritten async add-on: local control of Audioflow speaker switches over MQTT,
  Home Assistant MQTT discovery, broker configuration from the Supervisor MQTT
  service, UDP device discovery, and on-demand re-discovery.
