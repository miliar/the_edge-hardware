# Python CLI Application Guide
This is a test utility for The Edge hardware that allows you to:
- Scan for available Edge devices
- Connect to a selected device
- Monitor real-time weight measurements
- View battery status
- Track maximum weight (high score)


## Running the Application
```bash
python python_cli_app/ble_json_central.py
```

## Example Output
```
Scanning for Edge devices...
Found device: myedgedewood
Services: <BoundServiceList: 51ad213f-e568-4e35-84e4-67af89c79ef0>
Found device: myedgedevice
Services: <BoundServiceList: 51ad213f-e568-4e35-84e4-67af89c79ef0>

Available devices:
1: myedgedewood
2: myedgedevice

Select device (1-2) or 'r' to rescan: 2
Connected!
{'voltage': '75 %', 'weight': 1566}
{'voltage': '77 %', 'weight': 2344}
{'voltage': '76 %', 'weight': 3869}
{'voltage': '76 %', 'weight': 5126}
{'voltage': '76 %', 'weight': 5362}
{'voltage': '77 %', 'weight': 3700}
{'voltage': '76 %', 'weight': 1503}
High score: 6.37 kg
Last score: 5.126 kg
Power: 77 %
```
