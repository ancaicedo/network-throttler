import socket
import os
import subprocess
import time

#curl -sSL https://raw.githubusercontent.com/thombashi/tcconfig/master/scripts/installer.sh | sudo bash

def get_local_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_connected_ip():
    local_ip = get_local_ip_address()
    subnet = ".".join(local_ip.split(".")[:-1]) + "."
    result = os.popen(f"arp-scan --localnet --interface={get_local_interface()} | awk '/{subnet}/ {{print $1}}'").read()
    ips = result.strip().split("\n")
    return ips


def get_local_interface():
    interface = os.popen("ip route show | awk  '/default/ {print $5}'").read().strip()
    return interface


def throttle_download_rate_tc(ip_address, rate_kbps):
    """Throttle the download rate of a connection with a specified IP address."""
    subprocess.run(["tc", "qdisc", "add", "dev", "ens3", "root", "handle", "1:", "htb"], check=True)
    subprocess.run(
        ["tc", "class", "add", "dev", "ens3", "parent", "1:", "classid", "1:1", "htb", "rate", f"{rate_kbps}kbps"],
        check=True)
    subprocess.run(
        ["tc", "filter", "add", "dev", "ens3", "protocol", "ip", "parent", "1:0", "prio", "1", "u32", f"match", "ip",
         "dst", ip_address, "flowid", "1:1"], check=True)


def main():
    ip_to_throttle = get_connected_ip()
    print(ip_to_throttle)
    # rate_kbps = 100
    # throttle_download_rate_tc(ip_address, rate_kbps)
    # print(f"Throttled download rate of connection with IP address {ip_address} to {rate_kbps} kilobits per second.")


if __name__ == "__main__":
    main()
