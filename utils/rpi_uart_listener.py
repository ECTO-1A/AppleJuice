import serial
import subprocess

try:
    from app import bt_data_options
    script_location = 'app.py'
except ImportError:
    from ..app import bt_data_options
    script_location = '../app.py'

# Define the UART port and baud rate
uart_port = '/dev/ttyS0'  # Use '/dev/ttyAMA0' on older Raspberry Pi models
baud_rate = 115200

# Open the UART port
ser = serial.Serial(uart_port, baud_rate)

while True:
    # Read data from UART
    data = ser.readline().decode('utf-8').strip()

    # Check if the received data is "apple"
    if data.lower() in [_.lower() for _ in bt_data_options.values()]:
        print("Received 'apple'. Running airpodsmax.py...")

        # Run the app.py program using subprocess
        try:
            subprocess.run(['python', script_location, '--device-name', data], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running data: {e}")
    else:
        print(f"Received '{data}'")
