import sys
from scapy.all import ARP, Ether, srp
from prettytable import PrettyTable

def scan_network(interface):
    try:
        # Create ARP request
        arp = ARP(pdst="192.168.1.0/24")  # Replace with your network range

        # Create Ethernet frame
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")

        # Combine into a single packet
        packet = ether / arp

        # Send the packet and capture responses
        result = srp(packet, timeout=3, iface=interface, verbose=False)[0]

        devices = []
        for sent, received in result:
            devices.append({'IP': received.psrc, 'MAC': received.hwsrc})

        return devices

    except Exception as e:
        print(f"Error: {e}")
        return []

def print_devices(devices):
    table = PrettyTable(["IP Address", "MAC Address"])
    for device in devices:
        table.add_row([device['IP'], device['MAC']])
    print(table)

def main():
    if len(sys.argv) != 2:
        print("Usage: python network_radar.py <interface>")
        sys.exit(1)

    interface = sys.argv[1]
    print(f"Scanning network on interface {interface}...")

    devices = scan_network(interface)
    if devices:
        print_devices(devices)
    else:
        print("No devices found.")

if __name__ == "__main__":
    main()
