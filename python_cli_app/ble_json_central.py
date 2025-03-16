from ble_json_service import SensorService
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement


class BLEController:
    WEIGHT_THRESHOLD = 1000  # Threshold in grams
    SCAN_TIMEOUT = 5.0  # Scanning timeout in seconds

    def __init__(self):
        self.ble = BLERadio()
        self.connection = None
        self.high_score = 0
        self.last_score = 0
        self.last_score_toggle = True

    def scan_for_devices(self):
        """Scan for available Edge devices and return list of advertisements."""
        print("Scanning for Edge devices...")
        devices = []
        try:
            for advertisement in self.ble.start_scan(
                ProvideServicesAdvertisement, timeout=self.SCAN_TIMEOUT
            ):
                if SensorService in advertisement.services:
                    if advertisement not in devices:
                        print(f"Found device: {advertisement.complete_name}")
                        print(f"Services: {advertisement.services}")
                        devices.append(advertisement)
        finally:
            self.ble.stop_scan()
        return devices

    def select_device(self, devices):
        """Let user select a device from the list of found devices."""
        if not devices:
            print("No Edge devices found!")
            return None

        print("\nAvailable devices:")
        for i, device in enumerate(devices, 1):
            name = (
                device.complete_name
                if device.complete_name
                else f"Edge Device {device.address}"
            )
            print(f"{i}: {name}")

        while True:
            try:
                choice = input(
                    "\nSelect device (1-{}) or 'r' to rescan: ".format(len(devices))
                )
                if choice.lower() == "r":
                    return None
                choice = int(choice)
                if 1 <= choice <= len(devices):
                    return devices[choice - 1]
                print(
                    f"Invalid choice. Please select a number between 1 and {len(devices)}"
                )
            except ValueError:
                print("Invalid input. Please enter a number or 'r'")

    def _handle_disconnected_state(self):
        """Handle device discovery and connection when disconnected."""
        devices = self.scan_for_devices()
        selected_device = self.select_device(devices)
        if selected_device:
            try:
                self.connection = self.ble.connect(selected_device)
                print("Connected!")
            except Exception as e:
                print(f"Failed to connect: {e}")
                self.connection = None
        else:
            print("\nScanning again...")

    def run(self):
        """Main loop for handling BLE connections and data."""
        while True:
            try:
                if not self.connection or not self.connection.connected:
                    self._handle_disconnected_state()
                    continue

                service = self.connection[SensorService]
                self.process_sensor_data(service)

            except Exception as e:
                print(f"Error: {e}")
                self.connection = None

    def _handle_active_weight(self, service):
        if self.last_score_toggle:
            self.last_score_toggle = False
            self.last_score = 0
        print(service.sensors)
        self.high_score = max(service.sensors.get("weight", 0), self.high_score)
        self.last_score = max(service.sensors.get("weight", 0), self.last_score)

    def _handle_inactive_weight(self, service):
        if not self.last_score_toggle:
            print(f"High score: {self.high_score / 1000} kg")
            print(f"Last score: {self.last_score / 1000} kg")
            print(f"Power: {service.sensors.get('voltage', '?')}")
            self.last_score_toggle = True

    def process_sensor_data(self, service):
        if service.sensors and service.sensors.get("weight", 0) > self.WEIGHT_THRESHOLD:
            self._handle_active_weight(service)
        else:
            self._handle_inactive_weight(service)


if __name__ == "__main__":
    controller = BLEController()
    controller.run()
