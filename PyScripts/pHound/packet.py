import scapy.all as scapy

def sniff_packets(interface):
    scapy.sniff(iface=interface, store=False, prn=process_packet)

def process_packet(packet):
    if packet.haslayer(scapy.IP):
        source_ip = packet[scapy.IP].src
        destination_ip = packet[scapy.IP].dst
        protocol = packet[scapy.IP].proto

        print(f"IP Packet: {source_ip} -> {destination_ip}, Protocol: {protocol}")

        if packet.haslayer(scapy.TCP):
            source_port = packet[scapy.TCP].sport
            destination_port = packet[scapy.TCP].dport
            print(f"TCP Segment: {source_ip}:{source_port} -> {destination_ip}:{destination_port}")

        elif packet.haslayer(scapy.UDP):
            source_port = packet[scapy.UDP].sport
            destination_port = packet[scapy.UDP].dport
            print(f"UDP Segment: {source_ip}:{source_port} -> {destination_ip}:{destination_port}")

# Replace 'eth0' with your network interface (use ifconfig or ipconfig to find your interface)
sniff_packets('wlan0')
