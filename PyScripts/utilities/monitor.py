from scapy.all import *

# Dictionary to store known devices (IP address: MAC address)
known_devices = {}

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1, 2):  # who-has or is-at
        ip_address = pkt[ARP].psrc
        mac_address = pkt[ARP].hwsrc
        if ip_address not in known_devices:
            known_devices[ip_address] = mac_address
            print(f"New device connected: IP = {ip_address}, MAC = {mac_address}")
            # Here you can implement further actions like sending an alert

def start_monitoring(interface):
    sniff(prn=arp_monitor_callback, filter="arp", iface=interface, store=0)

if __name__ == "__main__":
    # Replace 'eth0' with your network interface (e.g., 'en0' for macOS, 'eth0' or 'wlan0' for Linux)
    interface = 'wlan0'
    print(f"[*] Starting ARP monitoring on interface {interface}...")

    try:
        start_monitoring(interface)
    except KeyboardInterrupt:
        print("\n[*] User interrupted. Exiting...")
