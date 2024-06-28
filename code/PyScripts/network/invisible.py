import socket
import threading
from openvpn_api import VPN
import subprocess
import time

# Proxy server configuration
LOCAL_HOST = '127.0.0.1'  # Localhost
LOCAL_PORT = 8888          # Proxy port
REMOTE_HOST = 'www.example.com'  # Target server
REMOTE_PORT = 80           # Target server port

# VPN configuration
vpn_server = 'vpn.example.com'  # Replace with your VPN server address
vpn_username = 'your_username'  # Replace with your VPN username
vpn_password = 'your_password'  # Replace with your VPN password

def get_current_dns_servers():
    # Use subprocess to execute system commands to get current DNS servers
    try:
        ifconfig_output = subprocess.check_output(['ifconfig'], stderr=subprocess.STDOUT, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f'Error: {e}')
        return None
    
    dns_servers = set()
    lines = ifconfig_output.splitlines()
    for line in lines:
        if 'nameserver' in line:
            dns_server = line.split()[1]
            dns_servers.add(dns_server)
    
    return dns_servers

def check_dns_leak():
    # Get current DNS servers before connecting to VPN
    initial_dns_servers = get_current_dns_servers()
    if not initial_dns_servers:
        print('Failed to retrieve initial DNS servers.')
        return
    
    print(f'Initial DNS servers: {initial_dns_servers}')
    
    # Connect to VPN or desired network (simulate connecting to VPN)
    # Replace this with actual VPN connection code or manual connection to VPN
    
    # Wait for VPN connection to stabilize (simulate wait time)
    print('Simulating VPN connection...')
    time.sleep(5)  # Adjust wait time as necessary
    
    # Get DNS servers after connecting to VPN
    current_dns_servers = get_current_dns_servers()
    if not current_dns_servers:
        print('Failed to retrieve current DNS servers.')
        return
    
    print(f'Current DNS servers: {current_dns_servers}')
    
    # Compare initial and current DNS servers
    if initial_dns_servers != current_dns_servers:
        print('DNS leak detected! Your DNS servers have changed.')
    else:
        print('No DNS leak detected. Your DNS servers have not changed.')

def handle_client(client_socket):
    # Connect to the remote server
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((REMOTE_HOST, REMOTE_PORT))

    while True:
        # Receive data from the client
        client_data = client_socket.recv(4096)
        if not client_data:
            break
        
        # Send data to the remote server
        remote_socket.sendall(client_data)

        # Receive data from the remote server
        remote_data = remote_socket.recv(4096)
        if not remote_data:
            break
        
        # Send data back to the client
        client_socket.sendall(remote_data)

    # Close connections
    client_socket.close()
    remote_socket.close()

def start_proxy():
    # Create a TCP socket
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the local host and port
        proxy_socket.bind((LOCAL_HOST, LOCAL_PORT))
        
        # Listen for incoming connections
        proxy_socket.listen(5)
        print(f'[*] Proxy server is listening on {LOCAL_HOST}:{LOCAL_PORT}')

        while True:
            # Accept incoming client connections
            client_socket, addr = proxy_socket.accept()
            print(f'[*] Accepted connection from {addr[0]}:{addr[1]}')

            # Create a new thread to handle the client connection
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    
    except Exception as e:
        print(f'[-] Error: {e}')
    finally:
        # Close the proxy socket
        proxy_socket.close()



def connect_to_vpn(vpn_server, vpn_username, vpn_password):
    try:
        vpn = VPN(host='localhost', port=1337)  # Adjust host and port if necessary
        vpn.connect(vpn_server, vpn_username, vpn_password)
        print(f'Connected to VPN server: {vpn_server}')
    except Exception as e:
        print(f'Error: {e}')


if __name__ == '__main__':
    
    check_dns_leak()
    start_proxy()
    connect_to_vpn(vpn_server, vpn_username, vpn_password)# Replace with the new IP address you want to set