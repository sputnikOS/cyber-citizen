import socket
from concurrent.futures import ThreadPoolExecutor


banner = """

=======================================================================
                            Port Scanner
                    Usage: python port.py 
=======================================================================

"""

def scan_port(ip, port):
    """Attempt to connect to a specific port on the given IP address."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1)
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                service_name = socket.getservbyport(port, "tcp")
            except OSError:
                service_name = "Unknown service"
            return port, service_name
        return None

def scan_ports(ip, port_range=(1, 1024), max_workers=100):
    """Scan the specified range of ports on the given IP address."""
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(scan_port, ip, port) for port in range(port_range[0], port_range[1] + 1)]
        for future in futures:
            result = future.result()
            if result:
                open_ports.append(result)
    return open_ports

if __name__ == "__main__":
    banner
    target_ip = input("Enter the IP address to scan: ")
    start_port = int(input("Enter the starting port number: ") or 1)
    end_port = int(input("Enter the ending port number: ") or 1024)

    print(f"Scanning {target_ip} from port {start_port} to {end_port}...")

    open_ports = scan_ports(target_ip, port_range=(start_port, end_port))

    if open_ports:
        print(f"Open ports on {target_ip}:")
        for port, service in open_ports:
            print(f"Port {port}: {service}")
    else:
        print(f"No open ports found on {target_ip}.")
