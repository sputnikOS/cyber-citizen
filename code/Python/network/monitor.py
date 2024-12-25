import psutil

def list_network_interfaces():
    # Get the network interfaces
    interfaces = psutil.net_if_addrs()

    # Print the interfaces and their addresses
    for interface, addresses in interfaces.items():
        print(f"Interface: {interface}")
        for address in addresses:
            print(f"  Address Family: {address.family.name}")
            print(f"  Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast: {address.broadcast}")
            print()

if __name__ == "__main__":
    list_network_interfaces()
