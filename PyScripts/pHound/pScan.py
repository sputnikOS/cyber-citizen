#!/usr/bin/python3
import nmap3

f = open('banner.txt', 'r')
content = f.read()

nmap = nmap3.Nmap()
# scanner = nmap.Nm  


# def list_connected_devices():
 

    # # Scan the local network for devices
    # scanner.nmap_no_portscan('192.168.1.0/24')

    # # Extract the list of connected devices from the scan results
    # hosts = scanner.nmap_no_portscan()

    # # Print the list of connected devices
    # print("Connected devices on the network:")
    # for host in hosts:
    #     if 'mac' in scanner[host]['addresses']:
    #         mac_address = scanner[host]['addresses']['mac']
    #     else:
    #         mac_address = 'unknown'
    #     print(f"{scanner[host]['addresses']['ipv4']} ({mac_address})")

# Call the list_connected_devices function
# list_connected_devices()


print("pyscan")
print("Nmap Version: ", nmap.nmap_version_detection('127.0.0.1'))
print(content)

ip=input("enter ip: \n")
print("ip ", ip)
type(ip)

resp = input("please select scan type: 1) SYN 2) UDP 3) Comprehensive \n")
print("running ", resp)

# if resp == '1':
#     scanner.scan(ip, '1-1024', '-v -sS')
#     print(scanner.scaninfo())
#     print("ip status: ", scanner[ip].state())
#     print(scanner[ip].all_protocols())
#     print("Open ports: ", scanner[ip]['tcp'].keys())
# elif resp == '2':
#     scanner.scan(ip, '1-1024', '-v -sU')
#     print(scanner.scaninfo())
#     print("ip status: ", scanner[ip].state())
#     print(scanner[ip].all_protocols())
#     print("Open ports: ", scanner[ip]['udp'].keys())
# elif resp == '3':
#     scanner.scan(ip, '1-1024', '-v -sS -sC -A -O')
#     print(scanner.scaninfo())
#     print("ip status: ", scanner[ip].state())
#     print(scanner[ip].all_protocols())
#     print("Open ports: ", scanner[ip]['tcp'].keys())
# elif resp >= '3' or '0' :
#     exit() 