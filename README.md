```markdown
# Linux MAC Address Changer and Network Scanner

## Description
This tool allows users to change the MAC address of a specified network interface, revert it to the original MAC address, generate a random MAC address, and scan the network to display IP and MAC addresses of connected devices.

## Features
- Change MAC address of a specified network interface
- Revert to the original MAC address
- Generate a random MAC address
- Scan the network and display IP and MAC addresses of devices in a table format

## Requirements
- Python 3.x
- `prettytable` library
- `optparse` library
- `arp-scan` command-line tool



## Installation

### 1. Clone the repository
   ```bash
   git clone https://github.com/BBLVCKK/Lnx-Mac-Address-Changer.git
   ```

### 2. Navigate to the project directory
   ```bash
   cd Lnx-Mac-Address-Changer
   ```

### 3. Install required Python libraries
   You need to install the `prettytable` and `optparse` libraries:
   ```bash
   pip install prettytable optparse
   ```

### 4. Install `arp-scan`
   On **Debian/Ubuntu** systems, you can install `arp-scan` by running:
   ```bash
   sudo apt-get install arp-scan
   ```

   On **Fedora/RHEL** systems:
   ```bash
   sudo dnf install arp-scan
   ```

   For **Arch Linux** systems:
   ```bash
   sudo pacman -S arp-scan
   ```

## Usage
Run the script with **sudo** (as root privileges are required to change the MAC address):
   ```bash
   sudo python3 Lnx_MacAddress_Changer.py -i <interface> [options]
   ```

### Options:
- `-i` : Specify the network interface (e.g., eth0, wlan0)
- `-m` : Specify the new MAC address (manual input)
- `-o` : Revert to the original MAC address
- `-r` : Generate a random MAC address

### Examples:
- Change the MAC address:
   ```bash
   sudo python3 Lnx_MacAddress_Changer.py -i eth0 -m 00:11:22:33:44:55
   ```

- Revert to the original MAC address:
   ```bash
   sudo python3 Lnx_MacAddress_Changer.py -i eth0 -o
   ```

- Generate a random MAC address:
   ```bash
   sudo python3 Lnx_MacAddress_Changer.py -i eth0 -r
   ```
