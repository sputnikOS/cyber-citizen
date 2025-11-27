from scapy.all import ARP, sniff
from datetime import datetime

def process_packet(packet):
    """Process ARP packets to detect devices."""
    if ARP in packet and (packet[ARP].op == 1 or packet[ARP].op == 2):  # ARP request or reply
        mac_address = packet[ARP].hwsrc
        ip_address = packet[ARP].psrc
        print(f"[{datetime.now()}] Device detected: IP={ip_address}, MAC={mac_address}")

def monitor_network(interface):
    """Start sniffing on the specified network interface."""
    print(f"Monitoring network on interface: {interface}")
    print("Press Ctrl+C to stop.")
    try:
        sniff(filter="arp", prn=process_packet, iface=interface, store=0)
    except KeyboardInterrupt:
        print("\nStopping network monitor.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    interface = input("Enter the network interface to monitor (e.g., eth0, wlan0): ")
    monitor_network(interface)
