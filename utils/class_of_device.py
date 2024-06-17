import yaml

# https://bitbucket.org/bluetooth-SIG/public/src/main/assigned_numbers/core/class_of_device.yaml #7008105
cod_yaml = """cod_services:
 - bit: 13
   name: Limited Discoverable Mode
 - bit: 14
   name: LE audio
 - bit: 15
   name: Reserved for Future Use
 - bit: 16
   name: Positioning (Location identification)
 - bit: 17
   name: "Networking (LAN, Ad hoc, ...)"
 - bit: 18
   name: "Rendering (Printing, Speakers, ...)"
 - bit: 19
   name: "Capturing (Scanner, Microphone, ...)"
 - bit: 20
   name: "Object Transfer (v-Inbox, v-Folder, ...)"
 - bit: 21
   name: "Audio (Speaker, Microphone, Headset service, ...)"
 - bit: 22
   name: "Telephony (Cordless telephony, Modem, Headset service, ...)"
 - bit: 23
   name: "Information (WEB-server, WAP-server, ...)"
cod_device_class:
 - major: 0
   name: Miscellaneous
 - major: 1
   name: "Computer (desktop, notebook, PDA, organizer, ...)"
   minor:
    - value: 0
      name: Uncategorized (code for device not assigned)
    - value: 1
      name: Desktop Workstation
    - value: 2
      name: Server-class Computer
    - value: 3
      name: Laptop
    - value: 4
      name: Handheld PC/PDA (clamshell)
    - value: 5
      name: Palm-size PC/PDA
    - value: 6
      name: Wearable Computer (watch size)
    - value: 7
      name: Tablet
 - major: 2
   name: "Phone (cellular, cordless, pay phone, modem, ...)"
   minor:
    - value: 0
      name: Uncategorized (code for device not assigned)
    - value: 1
      name: Cellular
    - value: 2
      name: Cordless
    - value: 3
      name: Smartphone
    - value: 4
      name: Wired Modem or Voice Gateway
    - value: 5
      name: Common ISDN Access
 - major: 3
   name: LAN/Network Access Point
   subsplit: 3
   minor:
    - value: 0
      name: Fully available
    - value: 1
      name: "1% to 17% utilized"
    - value: 2
      name: "17% to 33% utilized"
    - value: 3
      name: "33% to 50% utilized"
    - value: 4
      name: "50% to 67% utilized"
    - value: 5
      name: "67% to 83% utilized"
    - value: 6
      name: "83% to 99% utilized"
    - value: 7
      name: No service available
   subminor:
    - value: 0
      name: Uncategorized (use this value if no others apply)
 - major: 4
   name: "Audio/Video (headset, speaker, stereo, video display, VCR, ...)"
   minor:
    - value: 0
      name: Uncategorized (code not assigned)
    - value: 1
      name: Wearable Headset Device
    - value: 2
      name: Hands-free Device
    - value: 3
      name: Reserved for Future Use
    - value: 4
      name: Microphone
    - value: 5
      name: Loudspeaker
    - value: 6
      name: Headphones
    - value: 7
      name: Portable Audio
    - value: 8
      name: Car Audio
    - value: 9
      name: Set-top box
    - value: 10
      name: HiFi Audio Device
    - value: 11
      name: VCR
    - value: 12
      name: Video Camera
    - value: 13
      name: Camcorder
    - value: 14
      name: Video Monitor
    - value: 15
      name: Video Display and Loudspeaker
    - value: 16
      name: Video Conferencing
    - value: 17
      name: Reserved for Future Use
    - value: 18
      name: Gaming/Toy
 - major: 5
   name: "Peripheral (mouse, joystick, keyboard, ...)"
   subsplit: 2
   minor:
    - value: 0
      name: Uncategorized (code not assigned)
    - value: 1
      name: Keyboard
    - value: 2
      name: Pointing Device
    - value: 3
      name: Combo Keyboard/Pointing Device
   subminor:
    - value: 0
      name: Uncategorized (code not assigned)
    - value: 1
      name: Joystick
    - value: 2
      name: Gamepad
    - value: 3
      name: Remote Control
    - value: 4
      name: Sensing Device
    - value: 5
      name: Digitizer Tablet
    - value: 6
      name: "Card Reader (e.g., SIM Card Reader)"
    - value: 7
      name: Digital Pen
    - value: 8
      name: "Handheld Scanner (e.g., barcodes, RFID)"
    - value: 9
      name: "Handheld Gestural Input Device (e.g., “wand” form factor)"
 - major: 6
   name: "Imaging (printer, scanner, camera, display, ...)"
   subsplit: 4
   minor_bits:
    - value: 4
      name: Display
    - value: 5
      name: Camera
    - value: 6
      name: Scanner
    - value: 7
      name: Printer
   subminor:
    - value: 0
      name: Uncategorized (default)
 - major: 7
   name: Wearable
   minor:
    - value: 1
      name: Wristwatch
    - value: 2
      name: Pager
    - value: 3
      name: Jacket
    - value: 4
      name: Helmet
    - value: 5
      name: Glasses
    - value: 6
      name: "Pin (e.g., lapel pin, broach, badge)"
 - major: 8
   name: Toy
   minor:
    - value: 1
      name: Robot
    - value: 2
      name: Vehicle
    - value: 3
      name: Doll/Action Figure
    - value: 4
      name: Controller
    - value: 5
      name: Game
 - major: 9
   name: Health
   minor:
    - value: 0
      name: Undefined
    - value: 1
      name: Blood Pressure Monitor
    - value: 2
      name: Thermometer
    - value: 3
      name: Weighing Scale
    - value: 4
      name: Glucose Meter
    - value: 5
      name: Pulse Oximeter
    - value: 6
      name: Heart/Pulse Rate Monitor
    - value: 7
      name: Health Data Display
    - value: 8
      name: Step Counter
    - value: 9
      name: Body Composition Analyzer
    - value: 10
      name: Peak Flow Monitor
    - value: 11
      name: Medication Monitor
    - value: 12
      name: Knee Prosthesis
    - value: 13
      name: Ankle Prosthesis
    - value: 14
      name: Generic Health Manager
    - value: 15
      name: Personal Mobility Device
 - major: 31
   name: "Uncategorized (device code not specified)\n"
"""

cod = yaml.load(cod_yaml, Loader=yaml.FullLoader)
