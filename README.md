# AppleJuice
#### Apple BLE Proximity Pairing Message Spoofing

> ### :red_circle: Disclaimer
> These scripts are an experimental PoC that uses Bluetooth Low Energy (BLE) to send proximity pairing messages to Apple devices.\
> This project is created for educational purposes and cannot be used for law violation or personal gain.
> The author of this project is not responsible for any possible harm caused by the materials of this project.

## Updates

**9/21/23** <br>
<br>
Thanks to [0DayCTF](https://github.com/0dayctf) the random option has been added!<br> 
<br>
*To run with random :* <br>
```python3 app.py --random``` <br>
*or* <br>
```python3 app.py -r -i 20``` <br>
to set to it to random and the time interval to 20ms, making it more spammy.<br>
<br>
**9/13/2023** <br>
<br>
After [Techryptic's attempt to steal the work of myself and WillyJL](https://techcrunch.com/2023/09/05/flipper-zero-hacking-iphone-flood-popups/), Willy has taken the time to give an insanely in-depth timeline of the events and proof of the work being stolen (Git and my typos dont lie!) Check out the full report below and please help us spread the word that the person who has been all over the news outlets claiming this as their work, stole the code and gave none of the actual developers credit.<br>
<br>
[The Controversy Behind Apple BLE Spam](https://willyjl.dev/blog/the-controversy-behind-apple-ble-spam)
### Flipper Zero

Thanks to the amazing work of [Willy-JL](https://github.com/Willy-JL/Willy-JL) this has been added to the [Flipper Zero Momentum Firmware](https://github.com/Next-Flip/Momentum-Firmware).
#### To install it now, follow the guide below from the Momentum Firmware page to clone and compile the current build that contains the Apple BLE Spam app.

> :warning: **Warning!** <br>
> We will not give basic support for compiling in our server. This is intended for people that already *know* what they are doing!

```bash
To download the repository:
$ git clone --recursive --jobs 8 https://github.com/Next-Flip/Momentum-Firmware.git
$ cd Momentum-Firmware/

To flash directly to the Flipper (Needs to be connected via USB, qFlipper closed)
$ ./fbt flash_usb_full

To compile a TGZ package
$ ./fbt updater_package

To build and launch a single app:
$ ./fbt launch APPSRC=your_appid
```

### ESP-32

Thanks to [ronaldstoner](https://github.com/ronaldstoner) for porting this over to the ESP-32

### Android

Check out this in-depth walk though by [Mobile Hacker](https://www.mobile-hacker.com/2023/09/07/spoof-ios-devices-with-bluetooth-pairing-messages-using-android/) about running AppleJuice on a rooted Android phone.

## About This Project
This was created in response to the various AppleTV spoof messages being sent out during [DEF CON 31](https://techcrunch.com/2023/08/14/researcher-says-they-were-behind-iphone-popups-at-def-con/). After experiencing it first hand, I had to figure out what was happening. The existing research projects I could find (see *credits*) had great info but were both a couple years out of date with broken package dependencies, so I decided to take what I could from them and start building from there.

## Hardware Requirements

To run these scripts you need a Linux machine with an internal Bluetooth card or a USB Bluetooth adapter.

All original testing was done on a Lenovo T480 with a built-in Bluetooth adapter.\
Later tested on Raspberry Pi 3B+ and Raspberry Pi Zero W running Kali Linux with a [Zexmte Long Range USB Bluetooth 5.1 Adapter with Dual Antenna](https://zexmte.com/collections/bluetooth-adapter/products/plug-play-long-range-bluetooth-5-1-usb-adapter).<br>

<img src="https://github.com/ECTO-1A/AppleJuice/assets/112792126/a6f2b9fa-ca26-45c1-a440-681beb55c76e" width="300"><br>

> **Range** <br>
> Range of messages by device type

| Device    | Range |
|:----------|:----------|
| Lenovo    | Couple feet from machine |
| Raspberry Pi and long range adapter   | 20+ feet indoors in heavy BLE traffic |

## Installation Instructions
Please follow in this exact order or you might run into issues with bluetooth dependencies.

### Clone the Main Repo
```bash
git clone https://github.com/ECTO-1A/AppleJuice.git && cd ./AppleJuice
```

### Install dependencies
```bash
sudo apt update && sudo apt install -y bluez libpcap-dev libev-dev libnl-3-dev libnl-genl-3-dev libnl-route-3-dev cmake libbluetooth-dev
```

### Dependencies requiring manual installation
> :warning: **Warning** <br>
> The `pybluez` library is broken on GitHub and needs to be installed manually
```bash
Download the latest version 
pip install git+https://github.com/pybluez/pybluez.git#egg=pybluez

pycrypto is not maintained, be sure to install pycryptodome instead 
pip install pycryptodome
```

### Install requirements
```bash
sudo pip install -r requirements.txt
```
### Execute scripts without `sudo`
> To be able to run without sudo, you need to set the capabilities of the python binary to allow it to access raw sockets. This is done with the following command 

```bash
sudo setcap cap_net_raw,cap_net_admin+eip $(eval readlink -f $(which python))
```

### Reboot Machine
Several users have reported the need for a reboot after installing the bluetooth packages in order for everything to work properly.

## Usage

#### Before running the script, check that your Bluetooth adapter is connected and showing as `hci0`
Run `hcitool dev` to get a list of connected adapters
```bash
hcitool dev
Devices:
    hci0    00:00:7C:00:3A:13
```
> :memo: **Note** <br>
> If the adapter is showing as `hci1` you will need to edit the `dev_id` variable in the scripts to match

### Available options

All messages have been combined into a single app. You can now run `app.py` to get a list of available options.<br>
To run the script use `-d (number of message)`  
> **Example** <br> 
> `app.py -d 13`

```python
python3 app.py
Please select a message option using -d.
Available message options:
1: Airpods
2: Airpods Pro
3: Airpods Max
4: Airpods Gen 2
5: Airpods Gen 3
6: Airpods Pro Gen 2
7: PowerBeats
8: PowerBeats Pro
9: Beats Solo Pro
10: Beats Studio Buds
11: Beats Flex
12: BeatsX
13: Beats Solo3
14: Beats Studio3
15: Beats Studio Pro
16: Beats Fit Pro
17: Beats Studio Buds+
18: AppleTV Setup
19: AppleTV Pair
20: AppleTV New User
21: AppleTV AppleID Setup
22: AppleTV Wireless Audio Sync
23: AppleTV Homekit Setup
24: AppleTV Keyboard
25: AppleTV 'Connecting to Network'
26: Homepod Setup
27: Setup New Phone
28: Transfer Number to New Phone
29: TV Color Balance
```

## Examples

`beatssolopro.py`
> **Model**: Beats Solo Pro

<img src="https://github.com/ECTO-1A/AppleJuice/assets/112792126/c3218a09-7aef-483b-957d-f3c19a55fc08" width="300">

`airpods_max.py`
> **Model**: Airpods Max

<img src="https://github.com/ECTO-1A/AppleJuice/assets/112792126/5eea40e8-d7c1-4324-9f3d-1425228d0458" width="300">

### Credit
- [FuriousMAC](https://github.com/furiousMAC/continuity) and [Hexway](https://github.com/hexway/apple_bleee) for all the prior research on Apple BLE, Continuity, and building the Wireshark disector.
- [Jae Bochs](https://infosec.exchange/@jb0x168/110879394826675242) for [exposing this to me at DEF CON 31](https://techcrunch.com/2023/08/14/researcher-says-they-were-behind-iphone-popups-at-def-con/) which made me jump into learning about BLE.
- Guillaume Celosia and Mathieu Cunche for reverse engineering [Proximity Pairing](https://petsymposium.org/2020/files/papers/issue1/popets-2020-0003.pdf") 

