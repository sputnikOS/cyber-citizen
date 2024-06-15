import scapy.all as scapy
import time
from scapy.layers.l2 import ARP, Ether
import socket

# NEEDS TO BE COMPLETED

def scan(ip):
    # Create an ARP request packet to get the MAC address of the IP
    arp_request = ARP(pdst=ip)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
    arp_request_broadcast = ether_frame / arp_request

    # Send the ARP request and receive the response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Extract MAC addresses from the response
    return [element[1].psrc for element in answered_list]


def get_current_devices(ip_range):
    devices_list = []
    try:
        answered_list = scan(ip_range)
        for element in answered_list:
            device_info = {"ip": element, "mac": get_mac_address(element)}
            devices_list.append(device_info)
    except Exception as e:
        print(f"Error: {e}")

    return devices_list


def get_mac_address(ip):
    # Create an ARP request packet to get the MAC address of the IP
    arp_request = ARP(pdst=ip)
    ether_frame = Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
    arp_request_broadcast = ether_frame / arp_request

    # Send the ARP request and receive the response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    # Extract the MAC address from the response
    return answered_list[0][1].hwsrc

def get_device_name(ip):
    try:
        device_name, _, _ = socket.gethostbyaddr(ip)
        return device_name
    except (socket.herror, socket.gaierror):
        return "Unknown"


def print_result(result_list):
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for element in result_list:
        print(element["ip"] + "\t\t" + element["mac"])

def main():
    ip_range = "127.0.0.1/24"  # Change this to your local network IP range

    known_devices = get_current_devices(ip_range)
    print("Known Devices:")
    print_result(known_devices)
    

    while True:
        time.sleep(60)  # Wait for 1 minute
        current_devices = get_current_devices(ip_range)

        new_devices = [device for device in current_devices if device not in known_devices]
        if new_devices:
            print("\nNew Devices Detected:")
            print_result(new_devices)
            known_devices += new_devices

if __name__ == "__main__":
    main()
