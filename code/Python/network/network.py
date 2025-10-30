import scapy.all as scapy
import socket

def scan(ip):
    # Create an ARP request to get MAC address of devices in the IP range
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    
    # Send the request and capture responses
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    devices_list = []
    for element in answered_list:
        device_info = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        devices_list.append(device_info)
    
    return devices_list

def display_result(devices_list):
    print("IP Address\t\tMAC Address")
    print("-----------------------------------------")
    for device in devices_list:
        print(f"{device['ip']}\t\t{device['mac']}")

if __name__ == "__main__":
    # Get the local network IP range (e.g., 192.168.1.1/24)
    local_ip = socket.gethostbyname(socket.gethostname())  # Get the local IP address
    ip_range = local_ip.rsplit('.', 1)[0] + '.1/24'  # Assume common subnet (192.168.x.1/24)

    # Perform a scan and display the results
    devices = scan(ip_range)
    display_result(devices)
