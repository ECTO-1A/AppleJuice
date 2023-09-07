import bluetooth
import time
import random

def advertise():
    print("Starting Beats Solo Pro advertising")
    # Combine all the data fields
    complete_data = data1 + left_speaker + right_speaker + case + data2
    ble.gap_advertise(interval, adv_data=bytes(complete_data))

# Initialize BLE
print("Initializing BLE...")
ble = bluetooth.BLE()
ble.active(True)

if ble.active():
    print("BLE is active")
else:
    print("Failed to activate BLE")

# Parameters
interval = 200

# Static data fields
data1 = (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0c, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45)
data2 = (0xda, 0x29, 0x58, 0xab, 0x8d, 0x29, 0x40, 0x3d, 0x5c, 0x1b, 0x93, 0x3a)

# Dynamic data fields (initial values)
left_speaker = (random.randint(1, 100),)
right_speaker = (random.randint(1, 100),)
case = (random.randint(128, 228),)

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
        
        # Update the dynamic data fields
        left_speaker = (random.randint(1, 100),)
        right_speaker = (random.randint(1, 100),)
        case = (random.randint(128, 228),)
        
        ble_reset_counter = 0

    advertise()
    time.sleep(2)
    ble_reset_counter += 1
