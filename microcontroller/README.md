# Microcontroller Setup Guide

## Initial Setup
1. Factory reset the device
2. Install UF2 bootloader
   - Follow [QT Py ESP32-S3 CircuitPython Guide](https://learn.adafruit.com/adafruit-qt-py-esp32-s3/circuitpython-2)
   - Use [Adafruit Web Serial ESPTool](https://adafruit.github.io/Adafruit_WebSerial_ESPTool/) for flashing

## File Deployment
Copy all files from the `microcontroller/` directory to the device, **excluding** the `setup_circuitpython/` folder.

## Directory Structure
```
microcontroller/
├── code.py                 # Main program file
├── ble_json_service.py     # BLE service implementation
├── config.json             # User configuration file
├── default_config.json     # Default configuration file
└── lib/                    # Required libraries
    ├── adafruit_ble/
    ├── adafruit_bus_device/
    ├── adafruit_register/
    ├── adafruit_pixelbuf.mpy
    ├── cedargrove_nau7802.mpy
    └── neopixel.mpy
```

## Operation Guide

### Serial Console Output
To monitor the serial output while usb-c connected:

1. Find the device ID:
```bash
ls /dev/tty.*
```

2. Connect to the serial console:
```bash
screen [device_id]
```

For more information on using the serial console, see the [CircuitPython Advanced Serial Console Guide](https://learn.adafruit.com/welcome-to-circuitpython/advanced-serial-console-on-mac-and-linux)


### LED Status Indicators
The onboard NeoPixel LED indicates the device's current status:
- Red: Error state or initializing
- Yellow: Waiting for BLE connection
- Green: Connected to a BLE device

### Sensor Functionality
The device provides two sensor measurements:
1. **Weight Sensor**: Uses the NAU7802 load cell amplifier to measure weight. The raw values are averaged over multiple samples (configurable) and scaled according to the configuration.
2. **Voltage Sensor**: Reads analog voltage from pin A2, converts it to a percentage based on configured offset and scale factors.

### BLE Service
The device advertises a custom BLE service with the following characteristics:

1. **Sensors Characteristic** (Read-only)
   - UUID: 528ff74b-fdb8-444c-9c64-3dd5da4135ae
   - Provides real-time sensor data in JSON format:
     ```json
     {
       "weight": <value>,
       "voltage": "<percentage>%"
     }
     ```

2. **Settings Characteristic** (Read/Write)
   - UUID: e077bdec-f18b-4944-9e9e-8b3a815162b4
   - Allows reading and updating device settings

### Configuration
The device uses a configuration file (`config.json`) with fallback to `default_config.json`. Configuration options include:
- `device_name`: BLE advertisement name
- `weight_samples`: Number of samples to average for weight measurement
- `weight_scale_factor`: Scaling factor for weight measurements
- `voltage`: Configuration for voltage sensor:
  - `offset`: Voltage reading offset
  - `scale_factor`: Voltage scaling factor
