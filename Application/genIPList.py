# from flask import Flask, jsonify, request
# import requests
import psutil
import socket
import ipaddress

#Current User ID
MYID=123

def generate_ip_list(local_ip, subnet_mask):
    network = ipaddress.IPv4Network(f'{local_ip}/{subnet_mask}', strict=False)
    ip_list = [str(ip) for ip in network.hosts()]
    ip_list.remove(local_ip)
    return ip_list


def get_subnet_mask():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.address == local_ip and addr.family == socket.AF_INET:
                return addr.netmask
    return "Subnet mask not found."

# print(get_base_ip())

def generate_IP_List():
    local_ip = socket.gethostbyname(socket.gethostname())  
    subnet_mask = get_subnet_mask()
    return generate_ip_list(local_ip, subnet_mask)


# print((generate_IP_List()))
