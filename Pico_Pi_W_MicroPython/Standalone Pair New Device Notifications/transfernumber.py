import bluetooth
import time

def advertise():
    print("Starting 'Transfer Number' Advertising")
    ble.gap_advertise(interval, adv_data=bytes(data1))

# Initialize BLE
ble = bluetooth.BLE()
ble.active(True)

# Check if BLE is active
if ble.active():
    print("BLE is active")
else:
    print("Failed to activate BLE")

# Parameters
interval = 200
data1 = (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc0, 0x02, 0x60, 0x4c, 0x95, 0x01, 0x00, 0x10, 0x00, 0x00, 0x00)

# Counter for BLE reset
ble_reset_counter = 0
ble_reset_threshold = 10

# Main Loop
while True:
    if ble_reset_counter >= ble_reset_threshold:
        print("Resetting BLE...")
        ble.active(False)
        time.sleep(1)
        ble.active(True)
        ble_reset_counter = 0

    advertise()
    time.sleep(2)
    ble_reset_counter += 1
