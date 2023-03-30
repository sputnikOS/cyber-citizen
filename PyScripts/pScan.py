#!/usr/bin/python3
import nmap
import sys

f = open('banner.txt', 'r')
content = f.read()

scanner = nmap.PortScanner()

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