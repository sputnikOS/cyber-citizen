import nmap

def list_connected_devices():
    # Create a new nmap scanner object
    nm = nmap.PortScanner()

    # Scan the local network for devices
    nm.scan(hosts='192.168.1.0/24', arguments='-sP')

    # Extract the list of connected devices from the scan results
    hosts = nm.all_hosts()

    # Print the list of connected devices
    print("Connected devices on the network:")
    for host in hosts:
        if 'mac' in nm[host]['addresses']:
            mac_address = nm[host]['addresses']['mac']
        else:
            mac_address = 'unknown'
        print(f"{nm[host]['addresses']['ipv4']} ({mac_address})")

# Call the list_connected_devices function
list_connected_devices()

## C:\python27\python.exe C:\utils\pyinstaller-2.0\pyinstaller.py --out=C:\shell\ --noconsole --onefile C:\shell.py