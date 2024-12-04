# NEEDS TO BE FIXED
from scapy.all import sniff 
import sys


# WORKING

banner = """

=======================================================================
                            Packet Sniffer
                    Usage: python sniff.py [wlan0/eth0]
=======================================================================

"""

def packet_callback(packet):
    try:
        print(f"Packet: {packet.summary()}")
    except Exception as e:
        print(f"Error processing packet: {e}")

def start_sniffing(interface):
    print(f"Sniffing on interface: {interface}")
    sniff(iface=interface, prn=packet_callback, store=False)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 sniff.py <interface>")
        sys.exit(1)
    
    network_interface = sys.argv[1]
    start_sniffing(network_interface)
