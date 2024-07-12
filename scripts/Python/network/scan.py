import scapy.all as scapy
import socket
import sys

#  Working

def scan_network(ip_range):
    # Create an ARP request packet to get the MAC address of the IP
    arp_request = scapy.ARP(pdst=ip_range)
    ether_frame = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast MAC address
    arp_request_broadcast = ether_frame / arp_request

    # Send the ARP request and receive the response
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]

    devices_list = []
    for element in answered_list:
        device_info = {
            "ip": element[1].psrc,
            "mac": element[1].hwsrc,
            "name": get_device_name(element[1].psrc)
        }
        devices_list.append(device_info)
    return devices_list

def get_device_name(ip):
    try:
        device_name = socket.gethostbyaddr(ip)[0]
    except (socket.herror, socket.gaierror):
        device_name = "Unknown"
    return device_name

def print_devices(devices_list):
    print("IP Address\t\tMAC Address\t\tDevice Name")
    print("--------------------------------------------------------------")
    for device in devices_list:
        print(f"{device['ip']}\t\t{device['mac']}\t\t{device['name']}")

if __name__ == "__main__":
    input = sys.argv[1]
    ip_range = input  # Adjust to your network range
    devices = scan_network(ip_range)
    print_devices(devices)