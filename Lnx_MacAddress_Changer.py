import subprocess
import optparse
import re
import random
import os
import sys
from prettytable import PrettyTable

# List of OUIs (first 6 bits)
OUI_LIST = [
    '50:c7:bf', '00:1b:78', '08:00:20', '3c:f7:32', '00:1a:11',
    '00:15:5d', '00:1b:67', '5c:5c:32', '78:44:7e', 'dc:a6:32',
    '00:1a:79', '00:e0:4c', '00:24:7c', '00:24:b6', '00:0c:29',
    'ac:22:05', '18:fe:34', '4c:55:70', '08:00:27', '50:46:5d',
    'c0:97:en', '00:17:c0', '00:24:37', '00:22:de', '00:25:b5',
    '00:27:18', '00:11:22', '28:fe:cc', '00:24:9c', '00:21:90'
]

developer_ascii_art = """
                _____ Dev Github: BBLVCKK _____
"""

def get_mac_address(interface):
    """Extract and return the current MAC address of a network interface."""
    try:
        ifconfig_result = subprocess.check_output(f"ifconfig {interface}", shell=True).decode("UTF-8")
        mac_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
        if mac_address:
            return mac_address[0]
        else:
            print(f"[-] Could not find MAC address for {interface}")
            return None
    except subprocess.CalledProcessError:
        print(f"[-] Failed to run ifconfig on {interface}")
        return None


def change_mac_address(interface, new_mac):
    """Change the MAC address of a network interface."""
    subprocess.call(f"ifconfig {interface} down", shell=True)
    subprocess.call(f"ifconfig {interface} hw ether {new_mac}", shell=True)
    subprocess.call(f"ifconfig {interface} up", shell=True)


def get_original_mac(interface):
    """Retrieve the original (permanent) MAC address using ethtool."""
    try:
        ethtool_result = subprocess.check_output(f"ethtool -P {interface}", shell=True).decode("UTF-8")
        original_mac = re.search(r"(?<=Permanent address: )\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ethtool_result)
        if original_mac:
            return original_mac[0]
        else:
            print(f"[-] Could not find original MAC address for {interface}")
            return None
    except subprocess.CalledProcessError:
        print(f"[-] Failed to run ethtool on {interface}")
        return None


def list_network_interfaces():
    """List all available network interfaces."""
    try:
        ifconfig_result = subprocess.check_output("ifconfig -a", shell=True).decode("UTF-8")
        interfaces = re.findall(r'^\w+', ifconfig_result, re.MULTILINE)
        print("[+] Available Network Interfaces:")
        for interface in interfaces:
            print(f" - {interface}")
    except subprocess.CalledProcessError:
        print("[-] Failed to retrieve network interfaces.")


def generate_random_mac():
    """Generate a random MAC address with a random OUI from the provided list."""
    # Select a random OUI (first 3 bytes)
    oui = random.choice(OUI_LIST)
    
    # Generate the last 3 bytes (6 hexadecimal characters) randomly
    random_mac_suffix = ':'.join(f"{random.randint(0, 255):02x}" for _ in range(3))
    
    return f"{oui}:{random_mac_suffix}"


def check_sudo():
    """Check if the script is run as root (sudo)."""
    if os.geteuid() != 0:
        print("[-] You need to run this script with sudo.")
        sys.exit(1)


def scan_network():
    """Scan the network and display MAC addresses in a table."""
    try:
        scan_result = subprocess.check_output("arp-scan -l", shell=True).decode("UTF-8")
        lines = scan_result.split('\n')
        
        table = PrettyTable()
        table.field_names = ["IP Address", "MAC Address", "Device Name"]

        for line in lines:
            if re.match(r'\d+\.\d+\.\d+\.\d+', line):
                parts = re.split(r'\s+', line.strip())
                if len(parts) >= 3:
                    ip_address = parts[0]
                    mac_address = parts[1]
                    device_name = ' '.join(parts[2:])
                    table.add_row([ip_address, mac_address, device_name])
        
        print("[+] Network Scan Results:")
        print(table)
    
    except subprocess.CalledProcessError:
        print("[-] Failed to run arp-scan.")
        return


def main():
    # Check if script is running as root
    check_sudo()

    # Print developer ASCII art
    print(developer_ascii_art)

    parser = optparse.OptionParser(usage="sudo Lnx_MacAddress_Changer.py [options]\n\nOptions:\n  -i  Specify the network interface\n  -m  Specify the new MAC address\n  -o  Revert to the original MAC address\n  -r  Generate a random MAC address\n  -s  Scan network devices and show MAC addresses")
    parser.add_option("-i","--interface", dest="network_interface", help="Specify the network interface (e.g., eth0)")
    parser.add_option("-m","--mac", dest="new_mac_address", help="Specify the new MAC address")
    parser.add_option("-o", action="store_true", dest="original", help="Revert to the original MAC address")
    parser.add_option("-r", action="store_true", dest="random_mac", help="Generate a random MAC address")
    parser.add_option("-s", action="store_true", dest="scan", help="Scan network and display MAC addresses")

    options, args = parser.parse_args()

    # If no options are provided, display the help message
    if not options.network_interface and not options.new_mac_address and not options.original and not options.random_mac and not options.scan:
        parser.print_help()
        return

    # List available network interfaces if only -i is provided without a network name
    if options.network_interface and not options.new_mac_address and not options.original and not options.random_mac and not options.scan:
        list_network_interfaces()
        return

    if options.scan:
        scan_network()
        return

    if not options.network_interface:
        print("[-] Please specify the network interface using the -i option.")
        return

    if options.original:
        original_mac = get_original_mac(options.network_interface)
        if original_mac:
            change_mac_address(options.network_interface, original_mac)
            print(f"[+] Successfully reverted MAC address for {options.network_interface} to {original_mac}")
        return

    if options.random_mac:
        options.new_mac_address = generate_random_mac()
        print(f"[+] Generated random MAC address: {options.new_mac_address}")

    if not options.new_mac_address:
        print("[-] Please specify the new MAC address using the -m option or use the -r option to generate a random MAC address.")
        return

    old_mac_address = get_mac_address(options.network_interface)
    if old_mac_address:
        change_mac_address(options.network_interface, options.new_mac_address)

        current_mac_address = get_mac_address(options.network_interface)
        print(f"[+] Successfully changed MAC address from {old_mac_address} to {options.new_mac_address} on {options.network_interface}.")


if __name__ == "__main__":
    main()
