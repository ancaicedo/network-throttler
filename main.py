import socket
import os

def get_local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

def get_connected_ips():
    local_ip = get_local_ip_address()
    subnet = ".".join(local_ip.split(".")[:-1]) + "."
    result = os.popen(f"arp-scan --localnet --interface={get_local_interface()} | awk '/{subnet}/ {{print $1}}'").read()
    ips = result.strip().split("\n")
    return ips

def get_local_interface():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[-1]

# Example usage
connected_ips = get_connected_ips()
print(connected_ips)