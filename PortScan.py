#!/usr/bin/env python3

from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
import socket, os, sys, subprocess, signal

def def_handler(sig, frame):
    print(f"{Style.DIM}{Fore.RED}\n\n[!] Exiting...\n{Style.RESET_ALL}")
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def scan_tcp(host, port, tcp_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.5)
    try:
        s.connect((host, port))
        print(f"{Style.DIM}{Fore.LIGHTGREEN_EX}TCP port {port} is open")
        tcp_ports.append(port)
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        s.close()

def scan_udp(host, port, udp_ports):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(1)
    try:
        s.sendto(b"\x00\x00", (host, port))
        data, addr = s.recvfrom(1024)
        print(f"{Style.DIM}{Fore.LIGHTYELLOW_EX}UDP port {port} is open")
        udp_ports.append(port)
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass
    finally:
        s.close()

def main():
    os.system("clear && figlet PortScan | lolcat")
    print(f"{Style.BRIGHT}{Fore.GREEN}Made by OusCyb3rH4ck\n{Style.RESET_ALL}")
    
    tcp_ports = []
    udp_ports = []
    
    host = input(f"{Style.BRIGHT}{Fore.MAGENTA}Enter the host to scan -> {Style.RESET_ALL}")

    ports = range(1, 65536)
    
    print("\n")
    
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda port: scan_tcp(host, port, tcp_ports), ports)
    
    ask_udp_scan = input(f"{Fore.YELLOW}{Style.BRIGHT}\nDo you want to scan UDP TOP 10.000 Ports? (y/n) -> {Style.RESET_ALL}")
    
    if ask_udp_scan == "y":
        print("\n")
        try:
            with open('udp_common_ports.txt', 'r') as file:
                udp_common_ports = [int(line.strip()) for line in file if line.strip().isdigit()]
        except FileNotFoundError:
            print(f"{Fore.RED}{Style.DIM}\n[!] File 'udp_common_ports.txt' not found\n{Style.RESET_ALL}")
            sys.exit(1)

        with ThreadPoolExecutor(max_workers=100) as executor:
            executor.map(lambda port: scan_udp(host, port, udp_ports), udp_common_ports)
    
    print(f"{Style.BRIGHT}{Fore.LIGHTCYAN_EX}\n[+] Scanning completed!{Style.RESET_ALL}")

    response_tcp = input(Fore.LIGHTMAGENTA_EX + Style.NORMAL + "\nDo you want to copy TCP ports? (y/n): ")
    if response_tcp == "y":
        tcp_ports_str = ",".join(map(str, tcp_ports))
        subprocess.run(["xclip", "-sel", "clip"], input=tcp_ports_str.encode(), check=True)
        print(Fore.GREEN + Style.BRIGHT + "\n[+] TCP ports copied to the clipboard!")
    else:
        print(Fore.RED + Style.DIM + "\n[-] TCP ports not copied")

    response_udp = input(Fore.LIGHTMAGENTA_EX + Style.NORMAL + "\nDo you want to copy UDP ports? (y/n): ")
    if response_udp == "y":
        udp_ports_str = ",".join(map(str, udp_ports))
        subprocess.run(["xclip", "-sel", "clip"], input=udp_ports_str.encode(), check=True)
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n[+] UDP ports copied to the clipboard!\n" + Fore.WHITE + Style.NORMAL)
    else:
        print(Fore.RED + Style.DIM + "\n[-] UDP ports not copied\n" + Style.NORMAL + Fore.WHITE)

if __name__ == '__main__':
    main()
