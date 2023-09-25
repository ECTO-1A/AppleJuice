# AppleJuice MicroPython Project Documentation
<video controls>
  <source src="./Media/AppleJuice_picopiw.webm" type="video/webm">
</video>


## Overview

This project is an adaptation of the [AppleJuice project](https://github.com/ECTO-1A/AppleJuice) to MicroPython, designed to work specifically with the Raspberry Pi Pico W. It includes two versions: a Command Line Interface (CLI) accessible from any terminal with REPL and a Web version that functions in modern web browsers.

### Hardware and Software Specifications

- MicroPython Version: MicroPython v1.20.0-487-g00930b213 (You can download the latest version from the [official website](https://micropython.org/). Make sure to choose the version for the Pico Pi W.)
- Raspberry Pi Pico W with RP2040
- Language: MicroPython

# AppleJuice MicroPython Project Versions

This project offers two versions: a Command Line Interface (CLI) and a Web Interface. You'll need to choose and copy the appropriate version to your Raspberry Pi Pico W.

## CLI Version

The CLI version provides a menu in your terminal REPL (Read-Eval-Print Loop) where you can select payloads and manage Bluetooth LE advertisements.

To use the CLI version:

1. Copy the CLI code to your Raspberry Pi Pico W's `main.py`.
2. Ensure your Pico W is connected to your computer.
3. Use Thonny or your preferred MicroPython development environment to upload the code to the Pico W.
4. Access the CLI menu from your terminal REPL to interact with the project.

## Web Version

The Web version allows you to control the project via a web interface accessible from modern web browsers. It offers two different configurations: Station Mode and Access Point (AP) Mode.

### Station Mode Configuration

To use the Web version in Station Mode:

1. Copy the Web code to your Raspberry Pi Pico W's `main.py`.
2. Configure your Wi-Fi credentials by editing the `st.json` file with your SSID and password.
3. Ensure your Pico W is connected to your computer.
4. Use Thonny or your preferred MicroPython development environment to upload the code to the Pico W.
5. Access the web interface by connecting your Pico W to your Wi-Fi network and finding its IP address. You can access it using a web browser.

### Access Point (AP) Mode Configuration

To use the Web version in Access Point (AP) Mode:

1. Copy the Web code to your Raspberry Pi Pico W's `main.py`.
2. Configure the AP mode by editing the `ap.json` file with your desired SSID and password.
3. Ensure your Pico W is connected to your computer.
4. Use Thonny or your preferred MicroPython development environment to upload the code to the Pico W.
5. Access the web interface by connecting your device to the Pico W's Wi-Fi network and finding its IP address. You can access it using a web browser.

Please use the appropriate configuration (`st.json` or `ap.json`) based on your chosen mode.
## Limitations of Raspberry Pi Pico W

The Raspberry Pi Pico W is a versatile microcontroller, but it does come with certain limitations that you should be aware of:

1. **Limited Wireless Range**: The Pico W has a built-in Wi-Fi module, but its wireless range is relatively short compared to dedicated Wi-Fi devices. This means that for remote operations, you'll need to be within a relatively close proximity to the device.

2. **Antenna Strength**: The onboard antenna of the Pico W is not very powerful, which can result in reduced signal strength and range. For optimal performance, it's best to operate the Pico W in environments with minimal interference.

3. **Web Server Performance**: When using the Pico W as a web server, it's important to understand that it has limited processing power and memory. Complex web applications or heavy traffic may lead to reduced responsiveness.

4. **Security Considerations**: As with any connected device, security is a concern. Make sure to secure your Pico W by changing default credentials, using encryption, and implementing access controls to prevent unauthorized access.

5. **Power Supply**: Ensure that your Pico W is adequately powered. Inadequate power can lead to instability and unexpected behavior.

6. **Responsibility**: When experimenting with the Pico W, especially in public places, be responsible and considerate of others' privacy and security. Avoid any activities that may be considered intrusive or harmful.

Remember that the Raspberry Pi Pico W is a fun and versatile platform for various projects, but it's important to use it responsibly and ethically, respecting privacy and legal boundaries.

## Notes

- This project is an adaptation in MicroPython of the original AppleJuice project available at [https://github.com/ECTO-1A/AppleJuice](https://github.com/ECTO-1A/AppleJuice).