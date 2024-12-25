import pyshark


def capture_packets(interface='eth0', packet_count=10):
    """
    Captures live packets from the specified network interface and prints their details.

    :param interface: The network interface to capture packets from (default is 'eth0').
    :param packet_count: The number of packets to capture.
    """
    # Capture live packets from the specified interface
    capture = pyshark.LiveCapture(interface=interface)
    
    print(f"Starting packet capture on interface: {interface}")
    
    for packet in capture.sniff_continuously(packet_count=packet_count):
        print_packet_details(packet)

def print_packet_details(packet):
    """
    Prints detailed information about a captured packet.

    :param packet: The packet to print details for.
    """
    try:
        print(f"\nPacket Number: {packet.number}")
        print(f"Timestamp: {packet.sniff_time}")
        print(f"Source Address: {packet.ip.src}")
        print(f"Destination Address: {packet.ip.dst}")
        print(f"Protocol: {packet.highest_layer}")
        print(f"Info: {packet.info}")
    except AttributeError as e:
        print(f"AttributeError: {e}")

if __name__ == "__main__":
    interface = 'eth0'  # Replace with your network interface (e.g., 'en0', 'wlan0')
    packet_count = 10   # Number of packets to capture
    capture_packets(interface, packet_count)
