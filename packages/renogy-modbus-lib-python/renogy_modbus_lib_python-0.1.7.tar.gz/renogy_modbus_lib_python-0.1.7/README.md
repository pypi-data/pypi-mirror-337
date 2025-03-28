# RenogyBT for Python SDK

RenogyBT is a Python SDK designed for Modbus communication with Renogy products. This project provides functionality to communicate with Renogy devices via Bluetooth.

## Project Structure

- `modbus_bt_pkg/src/renogy_lib_python/`: Contains the core library code.
- `modbus_bt_pkg/tests/`: Contains test code.

## Installation

Ensure your Python version is 3.6 or above. You can install the required dependencies using the following command:

```bash
pip install renogy-modbus-lib-python
```
## Usage
### Initialization
First, initialize the EnhancedModbusClient class to scan and connect to devices:

```python
from modbus_bt_pkg.src.renogy_lib_python import EnhancedModbusClient

async def main():
    client = EnhancedModbusClient(slave_address=0xFF)
    devices = await client.scan_devices()
    # Select and connect to a device
    success = await client.connect(selected_device['address'])
 ```

### Data Retrieval
Once connected, you can use the following methods to retrieve battery raw data and status information:

```python
response = await client.get_hole_original_data()

status = await client.get_status()
 ```

## Features
- Device Scanning : Use the scan_devices method to scan nearby Bluetooth devices.
- Device Connection : Use the connect method to connect to the selected device.
- Data Retrieval : Use the get_hole_original_data and get_status methods to obtain raw data and status information from the device.

## License
This project is licensed under the Renogy License. For more details, please refer to the https://www.renogy.com.