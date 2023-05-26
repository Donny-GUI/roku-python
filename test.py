import requests
import ping3
import scapy.all as scapy
from requests import get
from ipify import get_ip
from ipify.exceptions import IpifyException, ConnectionError, ServiceError


def mac_vendor(mac_address):
    url = f"https://api.macvendors.com/{mac_address}"
    response = requests.get(url)
    print("[mac address] ",mac_address)
    print("[mac vender] ", response.text)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Vendor not found"


def outward_ip():
    try:
        ip = get_ip()
    except ConnectionError:
        print("Connection Error")
        return None
    except ServiceError:
        print("Service Error")
        return None
    except:
        print("Unknown Error")
        return None 
    
    print('My public IP address is: {}'.format(ip))
    return ip

