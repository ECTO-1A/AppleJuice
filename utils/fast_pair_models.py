"""
All credits to https://github.com/DiamondRoPlayz/FastPair-Models
#dc712f0
"""


genuine_fp_models = {
    # Genuine devices, Discovered by @DiamondRoPlayz
    "Razer Hammerhead TWS X": 0x72EF8D,
    "Razer Hammerhead TWS": 0x0E30C3,
    "Test 00000D": 0x00000D,
    "Android Auto": [0x000007, 0x070000],
    "Foocorp Foophones": [0x000008, 0x080000],
    "Test Android TV": [0x000009, 0x090000],
    "Test 00000a - Anti-Spoofing": [0x00000A, 0x0A0000],
    "Google Gphones": [0x00000B, 0x0B0000, 0x0C0000],
    "Google Pixel Buds": [0x000006, 0x060000],
    "Fast Pair Headphones": [0x000048, 0x000049, 0x480000, 0x490000],
    "Test 000035": [0x000035, 0x350000],
    "LG HBS1110": 0x001000,
    "AIAIAI TMA-2 (H60)": 0x002000,
    "Libratone Q Adapt On-Ear": [0x003000, 0x003001],
    "Arduino 101": [0x000047, 0x470000],
    "Bose QuietComfort 35 II": [0x0000F0, 0x0100F0, 0xF00000],
    "T10": 0xF00400,
    "M&D MW65": 0x003B41,
    "Cleer FLOW Ⅱ": 0x003D8A,
    "Panasonic RP-HD610N": 0x005BC3,
    "soundcore Glow Mini": 0x008F7D,
    "boAt  Airdopes 621": 0x00A168,
    "Jabra Elite 2": 0x00AA48,
    "Beoplay E8 2.0": 0x00AA91,
    "Smart Controller 1": 0x00B727,
    "Sony WF-1000X": [0x00C95C, 0x01C95C],
    "Pioneer SE-MS9BN": 0x00FA72,
    "Nirvana Ion": 0x011242,
    "Cleer EDGE Voice": 0x013D8A,
    "Beoplay H9 3rd Generation": 0x01AA91,

    "BLE-Phone": 0x01E5CE,
    "WH-1000XM4": [0x01EEB4, 0x058D08],
    "Goodyear": 0x0200F0,
    "B&O Earset": 0x02AA91,
    "Sony WH-1000XM2": [0x02C95C, 0x03C95C, 0x06C95C, 0x07C95C],
    "ATH-CK1TW": 0x02D815,
    "TCL MOVEAUDIO S200": 0x02E2A9,
    "Plantronics PLT_K2": [0x035754, 0x045754],
    "PLT V8200 Series": [0x035764, 0x045764],
    "DENON AH-C830NCW": 0x038B91,
    "Beats Studio Buds": 0x038F16,
    "Michael Kors Darci 5e": 0x039F8F,
    "B&O Beoplay H8i": 0x03AA91,
    "YY2963": 0x03B716,
    "MOTO BUDS 135": 0x03C99C,
    "Writing Account Key": 0x03F5D4,

    "Beoplay H4": 0x04AA91,
    "Sony WI-1000X": [0x04C95C, 0x05C95C],
    "Major III Voice": 0x050F0C,
    "MINOR III": 0x052CC7,
    "Galaxy S23 Ultra": 0x0577B1,
    "TicWatch Pro 5": 0x057802,
    "Pixel Buds": [0x0582FD, 0x92BBBD],
    "WONDERBOOM 3": 0x05A963,
    "Galaxy S20+": 0x05A9BC,
    "B&O Beoplay E6": 0x05AA91,
    "Galaxy S21 5G": 0x06AE20,
    "OPPO Enco Air3 Pro": 0x06C197,
    "soundcore Liberty 4 NC": 0x06D8FC,
    "Technics EAH-AZ60M2": 0x0744B6,

    "WF-C700N": 0x07A41C,
    "Nest Hub Max": 0x07F426,

    # JBL devices, Discovered by @DiamondRoPlayz
    "JBL Everest 110GA - Gun Metal": [0xF00200, 0x0002F0, 0xF00201, 0x0102F0],
    "JBL Everest 110GA - Silver": [0xF00202, 0x0202F0],

    "JBL Everest 310GA - Brown": [0xF00203, 0x0302F0],
    "JBL Everest 310GA - Gun Metal": [0xF00204, 0x0402F0],
    "JBL Everest 310GA - Silver": [0xF00205, 0x0502F0],
    "JBL Everest 310GA - Purple": [0xF00206, 0x0602F0],

    "JBL Everest 710GA - Gun Metal": [0xF00207, 0x0702F0],
    "JBL Everest 710GA - Silver": [0xF00208, 0x0802F0],

    "JBL LIVE400BT - Black": [0xF00209, 0xF0020D],
    "JBL LIVE400BT - White": 0xF0020A,
    "JBL LIVE400BT - Blue": 0xF0020B,
    "JBL LIVE400BT - Red": 0xF0020C,

    "JBL LIVE500BT - Black": [0xF0020E, 0xF00212],
    "JBL LIVE500BT - White": 0xF0020F,
    "JBL LIVE500BT - Blue": 0xF00210,
    "JBL LIVE500BT - Red": 0xF00211,

    "JBL LIVE650BTNC - Black": 0xF00213,
    "JBL LIVE650BTNC - White": 0xF00214,
    "JBL LIVE650BTNC - Blue": 0xF00215,

    "JBL REFLECT MINI NC": 0x02D886,
    "JBL TUNE770NC": 0x02DD4F,
    "JBL LIVE FLEX": 0x02F637,
    "JBL TUNE760NC": 0x038CC7,

    "JBL WAVE BEAM - Blue": 0x04ACFC,
    "JBL TUNE 720BT": 0x04AFB8,
    "JBL TUNE125TWS": 0x054B2D,
    "JBL LIVE220BT": 0x05C452,
    "JBL LIVE770NC": 0x0660D7,

    # LG devices, Discovered by @DiamondRoPlayz
    "LG HBS-835S": [0xF00300, 0x0003F0],
    "LG HBS-835": [0xF00301, 0x0103F0],
    "LG HBS-830": [0xF00302, 0x0203F0],
    "LG HBS-930": [0xF00303, 0x0303F0],
    "LG HBS-1010": [0xF00304, 0x0403F0],
    "LG HBS-1500": [0xF00305, 0x0503F0],
    "LG HBS-1700": [0xF00306, 0x0603F0],
    "LG HBS-1120": [0xF00307, 0x0703F0],
    "LG HBS-1125": [0xF00308, 0x0803F0],
    "LG HBS-2000": [0xF00309, 0x0903F0],

    # Genuine devices, Discovered by @Willy-JL and @Spooks4576
    "Bose NC 700": 0xCD8256,
    "JBL Buds Pro": 0xF52494,
    "JBL Live 300TWS": 0x718FA4,
    "JBL Flip 6": 0x821F66,
    "Sony XM5": 0xD446A7,
    "Sony WF-1000XM4": 0x2D7A23,

    # Genuine devices, Discovered by @xAstroBoy
    "Soundcore Spirit Pro GVA": 0x72FB00,
    "Bisto CSR8670 Dev Board": 0x0001F0,  # non visible and breaks network

    # Genuine actions, Discovered by @Mr-Proxy-source
    "Set Up Device aka Google Gphones": 0x00000C,
}

custom_fp_models = {
    # Custom debug popups, Created by @DiamondRoPlayz
    "Obama": 0x7C6CDB,
    "Ryanair": 0x005EF9,
    "FBI": 0xE2106F,
    "Tesla": 0xB37A62,

    # Custom debug popups from flipper rom
    "Flipper Zero": 0xD99CA1,
    "Free Robux": 0x77FF67,
    "Free VBucks": 0xAA187F,
    "Rickroll": 0xDCE9EA,
    "Animated Rickroll": 0x87B25F,  # non visible and breaks network
    "Boykisser": 0xF38C02,
    "BLM": 0x1448C9,
    "Xtreme": 0xD5AB33,
    "Xtreme Cta": 0x0C0B67,
    "Talking Sasquach": 0x13B39D,
    "ClownMaster": 0xAA1FE1,  # non visible and breaks network

    "Mobile Hacker": 0x3D45DC,

    # My own custom debug popups
    "Durka": 0x6B4025,
}

all_fp_models= genuine_fp_models | custom_fp_models
