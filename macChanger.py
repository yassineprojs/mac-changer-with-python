#!/usr/bin/env python

import subprocess
import argparse
import re


def change_mac(interface, new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


parser = argparse.ArgumentParser(description="Change the MAC address of a network interface.")
parser.add_argument("-i", "--interface", dest="interface", required=True, help="Interface to change its MAC address")
parser.add_argument("-m", "--mac", dest="new_mac", required=True, help="New MAC address")


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode('utf-8')

    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_result)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("could not read mac address")


# Parse the arguments
args = parser.parse_args()

interface = args.interface
new_mac = args.new_mac

current_mac = get_current_mac(args.interface)
print("Current MAc = "+str(current_mac))

change_mac(args.interface,args.new_mac)
current_mac = get_current_mac(args.interface)
if current_mac == args.new_mac:
    print("MAC address was successfully changed to " + current_mac)
else:
    print("MAC address did nit change")