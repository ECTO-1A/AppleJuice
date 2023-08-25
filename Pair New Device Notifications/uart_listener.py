import serial
import subprocess

# Define the UART port and baud rate
uart_port = '/dev/ttyS0'  # Use '/dev/ttyAMA0' on older Raspberry Pi models
baud_rate = 115200

# Open the UART port
ser = serial.Serial(uart_port, baud_rate)

while True:
    # Read data from UART
    data = ser.readline().decode('utf-8').strip()
    
    # Check if the received data is "apple"
    if data == "max":
        print("Received 'apple'. Running airpodsmax.py...")
        
        # Run the airpodsmax.py program using subprocess
        try:
            subprocess.run(['python', 'airpodsmax.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running airpodsmax.py: {e}")

    # Check if the received data is "beatsx"
    elif data == "beatsx":
        print("Received 'beatsx'. Running beatsx.py...")
        try:
            subprocess.run(['python', 'beatsx.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running beatsx.py: {e}")
        
    # Check if the received data is "beatsx"
    elif data == "beatssolopro":
        print("Received 'beatssolopro'. Running beatssolopro.py...")
        try:
            subprocess.run(['python', 'beatssolopro.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running beatssolopro.py: {e}")
    
    # Check if the received data is "beatsx"
    elif data == "airpods":
        print("Received 'airpods'. Running airpods.py...")
        try:
            subprocess.run(['python', 'airpods.py'], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running airpods.py: {e}")

    else:
        print(f"Received '{data}'")