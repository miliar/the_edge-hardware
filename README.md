# The Edge - Hardware


This repository contains the hardware implementation of The Edge, a BLE-enabled weight sensor designed specifically for climbing training.

<img src="pics/edge.jpg" alt="The Edge Device" width="500"/>

## Project Overview

```mermaid
graph LR
    A[The Edge Hardware] --> |BLE| B[The Edge - Climbing Game]
    subgraph Hardware
        C[Load Cell Sensor] --> A
        E[ESP32-S3 Controller] --> A
    end
    subgraph Mobile App
        B --> F[Game Interface]
        B --> G[Training Stats]
        B --> H[Level Editor]
    end
```

## Project Structure

- [/board](board/README.md) - Hardware assembly instructions and component list
- [/microcontroller](microcontroller/README.md) - Firmware implementation and setup guide
- [/python_cli_app](python_cli_app/README.md) - Test utility (for development use)

## Mobile Application

The Edge hardware connects to "The Edge - Climbing Game" mobile application (available for iOS and Android), which transforms your climbing training into an interactive gaming experience. The app features real-time strength feedback, a progressive level system, and custom level creation capabilities, allowing you to turn training protocols into engaging challenges.

### App Demo

Check out the app in action:

<a href="https://youtube.com/shorts/Y2iQzmk7Qgc" target="_blank">
    <img src="https://img.youtube.com/vi/Y2iQzmk7Qgc/maxresdefault.jpg" width="500"/>
</a>

### App Screenshots

<img src="pics/app/app1.PNG" width="200"/> <img src="pics/app/app2.PNG" width="200"/> <img src="pics/app/app3.PNG" width="200"/> <img src="pics/app/app4.PNG" width="200"/>

## Getting Started

1. Follow the [hardware assembly guide](board/README.md) to build the device
2. Set up the [microcontroller firmware](microcontroller/README.md)
3. Install The Edge - Climbing Game from your device's app store
4. Connect the app to your Edge hardware via Bluetooth
5. Start training!

## Repository Contents

- `board/` - 3D models, assembly instructions, and parts list
- `microcontroller/` - CircuitPython firmware and configuration
- `pics/` - Project documentation images
- `python_cli_app/` - Test utility (for development use)
