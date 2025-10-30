import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor

def scan_ip(ip, port):
    """Check if a port on an IP address is open."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Timeout in seconds
            s.connect((ip, port))
            return f"{ip}:{port} is open"
    except:
        return None

def scan_network(network, ports):
    """Scan a network for open ports."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        tasks = [
            executor.submit(scan_ip, str(ip), port)
            for ip in ipaddress.IPv4Network(network, strict=False)
            for port in ports
        ]
        for task in tasks:
            result = task.result()
            if result:
                open_ports.append(result)
    return open_ports

if __name__ == "__main__":
    print("IP Scanner")
    network = input("Enter the network (e.g., 192.168.1.0/24): ")
    ports_input = input("Enter the ports to scan (comma-separated, e.g., 80,443): ")
    ports = [int(port.strip()) for port in ports_input.split(",")]

    print(f"Scanning network: {network}")
    print(f"Scanning ports: {ports}")
    results = scan_network(network, ports)

    if results:
        print("\nOpen ports found:")
        for result in results:
            print(result)
    else:
        print("\nNo open ports found.")
    