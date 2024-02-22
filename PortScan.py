#!/usr/bin/env python3

from colorama import Fore, Style
import socket
import os
import sys
import struct
import concurrent.futures
import subprocess
import signal

def handler(sig, frame):
    print(Fore.RED + Style.DIM + "\n\n[!] Exiting...\n" + Fore.WHITE + Style.NORMAL)
    sys.exit(1)

signal.signal(signal.SIGINT, handler)

tcp_ports = []
udp_ports = []

def scan_tcp(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        print(Fore.GREEN + Style.DIM + f"TCP port {port} is open")
        tcp_ports.append(str(port))
        s.close()
    except:
        pass

def scan_udp(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0.5)
    if port == 53:
        data = struct.pack("!HHHHHH", 1, 0, 1, 0, 0, 0)
        data += b"\x03www\x07example\x03com\x00"
        data += struct.pack("!HH", 1, 1)
    else:
        data = b""
    s.sendto(data, (host, port))
    try:
        data, addr = s.recvfrom(1024)
        print(Fore.YELLOW + f"UDP port {port} is open")
        udp_ports.append(str(port))
        s.close()
    except socket.timeout:
        pass
    except socket.error as e:
        print(f"Error on UDP port {port}: {e}")
        pass

if __name__ == '__main__':
    
    os.system("clear && figlet Port Scan | lolcat")
    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "Made by OusCyb3rH4ck\n" + Fore.WHITE + Style.NORMAL)
    
    host = input(Fore.MAGENTA + Style.BRIGHT + "Enter the host to scan: " + Fore.WHITE + Style.NORMAL)
    print("\n")
    
    os.system("ulimit -n 5100")
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=5000)

    executor.map(scan_tcp, [host] * 65535, range(1, 65536))
    print("\n")
    executor.map(scan_udp, [host] * 65535, range(1, 65536))

    executor.shutdown(wait=True)

    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n[+] Scanning completed!")

    response_tcp = input(Fore.LIGHTMAGENTA_EX + Style.NORMAL + "\nDo you want to copy TCP ports? (y/n): ")

    if response_tcp == "y":
        tcp_ports_str = ",".join(tcp_ports)
        subprocess.run(["xclip", "-sel", "clip"], input=tcp_ports_str.encode(), check=True)
        print(Fore.GREEN + Style.BRIGHT + "\n[+] TCP ports copied to the clipboard!")
    else:
        print(Fore.RED + Style.DIM + "\n[-] TCP ports not copied")

    response_udp = input(Fore.LIGHTMAGENTA_EX + Style.NORMAL + "\nDo you want to copy UDP ports? (y/n): ")

    if response_udp == "y":
        udp_ports_str = ",".join(udp_ports)
        subprocess.run(["xclip", "-sel", "clip"], input=udp_ports_str.encode(), check=True)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n[+] UDP ports copied to the clipboard!\n" + Fore.WHITE + Style.NORMAL)
    else:
        print(Fore.RED + Style.DIM + "\n[-] UDP ports not copied\n" + Style.NORMAL + Fore.WHITE)
