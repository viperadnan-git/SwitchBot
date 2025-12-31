# SwitchBot

A home automation system that turns electrical appliances into smart devices using ESP32 microcontrollers and a cloud-based WebSocket server.

## Overview

SwitchBot allows you to control up to 8 electrical relays remotely via a REST API or WebSocket connection. The system consists of two parts:

1. **Hardware (ESP32 Firmware)** - Arduino sketch that runs on ESP32, handles relay control, manual switches, and WebSocket communication
2. **Backend Server (Python)** - Async web server using aiohttp that manages device connections and provides REST API endpoints

## Features

- Control up to 8 relays per device
- Manual switch override support (physical buttons)
- WiFi configuration via captive portal (WiFiManager)
- Secure WebSocket communication (SSL/TLS)
- REST API for integration with other services
- Persistent state storage using ESP32 Preferences
- Factory reset functionality
- Real-time bidirectional communication

## Tech Stack

### Hardware
- ESP32 microcontroller
- Arduino framework
- Libraries:
  - WiFiManager - Captive portal for WiFi setup
  - WebSocketsClient - WebSocket communication
  - ArduinoJson - JSON parsing
  - Preferences - Non-volatile storage

### Backend
- Python 3
- aiohttp - Async HTTP/WebSocket server
- aiohttp-jinja2 - Template rendering
- Cerberus - Data validation

## Hardware Pin Configuration

| Function | Pins |
|----------|------|
| Relay Outputs | GPIO 23, 22, 21, 19, 18, 5, 25, 26 |
| Switch Inputs | GPIO 13, 12, 14, 27, 33, 32, 15, 4 |
| Board LED | GPIO 2 |
| Reset Button | GPIO 17 |

## API Endpoints

### GET `/api/{device_key}`
Returns the current state of all relays for a device.

**Response:**
```json
{
  "relay_1": true,
  "relay_2": false,
  ...
}
```

### POST `/api/{device_key}`
Update relay states for a device.

**Request Body:**
```json
{
  "relay_1": true,
  "relay_2": false
}
```

**Response:**
```json
{
  "status": true,
  "data": { "relay_1": true, "relay_2": false }
}
```

### WebSocket `/ws/{device_key}`
Real-time bidirectional communication for device control and state updates.

## Setup

### Hardware Setup

1. Flash the Arduino sketch to your ESP32
2. On first boot, connect to the "SwitchBot" WiFi network
3. Configure your WiFi credentials and SwitchBot username/password
4. The device will connect to the server automatically

### Server Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python -m app
   ```

## How It Works

1. **Device Boot**: ESP32 loads stored credentials or starts captive portal for configuration
2. **Connection**: Device establishes SSL WebSocket connection to the server
3. **Registration**: Server registers the device in `ACTIVE_DEVICES` dictionary
4. **Control**: Users send commands via REST API or WebSocket
5. **Execution**: Server forwards commands to the device via WebSocket
6. **Feedback**: Device reports state changes back to the server
7. **Manual Override**: Physical switches can toggle relays locally, state syncs to server

## Architecture

```
┌─────────────┐     WebSocket     ┌─────────────┐     REST API     ┌─────────────┐
│   ESP32     │◄──────────────────►│   Server    │◄─────────────────►│   Client    │
│  (Device)   │      (SSL)        │  (aiohttp)  │                   │  (App/Web)  │
└─────────────┘                   └─────────────┘                   └─────────────┘
      │                                  │
      │ Manual                           │ State
      │ Switches                         │ Storage
      ▼                                  ▼
┌─────────────┐                   ┌─────────────┐
│   Relays    │                   │  Database   │
│ (Appliances)│                   │             │
└─────────────┘                   └─────────────┘
```

## License

GPL-3.0

## Author

[viperadnan](https://github.com/viperadnan-git)
