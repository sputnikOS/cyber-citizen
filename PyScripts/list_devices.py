import nmap

def list_devices_on_network():
    nm = nmap3.PortScanner()
    nm.scan(hosts='127.0.0.1', arguments='-sn')
    
    for host in nm.all_hosts():
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]['addresses']['mac']
            ip_address = nm[host]['addresses']['ipv4']
            vendor = nm[host]['vendor'][mac_address]
            print(f"IP Address: {ip_address} | MAC Address: {mac_address} | Vendor: {vendor}")

# Example usage
list_devices_on_network()