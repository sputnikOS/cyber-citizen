#!/usr/bin/python3
import nmap

f = open('banner.txt', 'r')
content = f.read()

scanner = nmap.PortScanner()


def list_connected_devices():
 

    # Scan the local network for devices
    scanner.scan(hosts='192.168.1.0/24', arguments='-sP')

    # Extract the list of connected devices from the scan results
    hosts = scanner.all_hosts()

    # Print the list of connected devices
    print("Connected devices on the network:")
    for host in hosts:
        if 'mac' in scanner[host]['addresses']:
            mac_address = scanner[host]['addresses']['mac']
        else:
            mac_address = 'unknown'
        print(f"{scanner[host]['addresses']['ipv4']} ({mac_address})")

# Call the list_connected_devices function
list_connected_devices()


print("pyscan")
print("Nmap Version: ", scanner.nmap_version())
print(content)

ip=input("enter ip: \n")
print("ip ", ip)
type(ip)

resp = input("please select scan type: 1) SYN 2) UDP 3) Comprehensive \n")
print("running ", resp)

if resp == '1':
    scanner.scan(ip, '1-1024', '-v -sS')
    print(scanner.scaninfo())
    print("ip status: ", scanner[ip].state())
    print(scanner[ip].all_protocols())
    print("Open ports: ", scanner[ip]['tcp'].keys())
elif resp == '2':
    scanner.scan(ip, '1-1024', '-v -sU')
    print(scanner.scaninfo())
    print("ip status: ", scanner[ip].state())
    print(scanner[ip].all_protocols())
    print("Open ports: ", scanner[ip]['udp'].keys())
elif resp == '3':
    scanner.scan(ip, '1-1024', '-v -sS -sC -A -O')
    print(scanner.scaninfo())
    print("ip status: ", scanner[ip].state())
    print(scanner[ip].all_protocols())
    print("Open ports: ", scanner[ip]['tcp'].keys())
elif resp >= '3' or '0' :
    exit() 