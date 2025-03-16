import json
from ble_json_service import SensorService
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from cedargrove_nau7802 import NAU7802
import board
import neopixel
import analogio


class LEDColors:
    ERROR = (255, 0, 0)
    WAITING = (255, 255, 0)
    CONNECTED = (0, 100, 0)


def load_config():
    """Load configuration from config.json file, falling back to default_config.json"""
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except (OSError, ValueError):
        with open("default_config.json", "r") as f:
            return json.load(f)


def zero_channel(nau):
    """Initiate internal calibration for current channel.Use when scale is started,
    a new channel is selected, or to adjust for measurement drift. Remove weight
    and tare from load cell before executing."""
    print(f"channel {nau.channel} calibrate.INTERNAL: {nau.calibrate('INTERNAL'):>5}")
    print(f"channel {nau.channel} calibrate.OFFSET:   {nau.calibrate('OFFSET'):>5}")
    print(f"...channel {nau.channel} zeroed")


def get_weight(nau, config):
    """Read and average consecutive raw sample values. Return average raw value."""
    sample_sum = 0
    for _ in range(config["weight_samples"]):
        while not nau.available():
            pass
        sample_sum += nau.read()
    return int((sample_sum / config["weight_samples"]) / config["weight_scale_factor"])


def get_voltage(pin, config):
    voltage_config = config["voltage"]
    return f"{int((pin.value - voltage_config['offset']) / voltage_config['scale_factor'])} %"


if __name__ == "__main__":
    print("Remove weights from load cell")
    pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pixel.fill(LEDColors.ERROR)
    config = load_config()
    ble = BLERadio()
    ble.name = config["device_name"]
    service = SensorService()
    advertisement = ProvideServicesAdvertisement(service)
    nau7802 = NAU7802(board.STEMMA_I2C(), address=0x2A, active_channels=1)
    enabled = nau7802.enable(True)
    zero_channel(nau7802)
    analog_pin = analogio.AnalogIn(board.A2)
    print("Ready")

    while True:
        pixel.fill(LEDColors.WAITING)
        print("Advertise services")
        ble.stop_advertising()
        print(f"Advertising with name: {ble.name}")
        print(f"Advertisement: {advertisement}")
        ble.start_advertising(advertisement)
        print("Waiting for connection...")

        while not ble.connected:
            pass

        print("Connected")
        pixel.fill(LEDColors.CONNECTED)
        while ble.connected:
            measurement = {
                "weight": get_weight(nau7802, config),
                "voltage": get_voltage(analog_pin, config),
            }
            service.sensors = measurement
            print(f"Sensors: {measurement}")
        print("Disconnected")
