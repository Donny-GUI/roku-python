import socket  
import subprocess 
import re
from threading import Thread


class LocalNetwork(object):
    def __init__(self) -> None:
        self.hosts = {}
        self.ip = None
        self.network_range = None
        self.addresses = []
    
    def get_network_addresses(self):
        ip = self.get_ip()
        bits = ip.split(".")[:-1]        
        _start = ".".join(bits)
        self.addresses = [f"{_start}.{x}" for x in range(1, 256)] 
        return self.addresses
    
    def get_network_range(self):
        ip = self.get_ip()
        _start = ".".join(ip.split(':')[:-1])
        self.addresses = [f"{_start}.{x}" for x in range(1, 256)] 
        start = _start + ".1/24"
        self.network_range = start
        return start
        
    def get_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip_address = s.getsockname()[0]
            print(ip_address)
            s.close()
            self.ip = ip_address
            return ip_address
        except socket.error:
            print("failed")
            s.close()
            return "Unable to retrieve IP address"

    def ip_to_hostname(self, ip):
        try:
            hostname = socket.gethostbyaddr(ip)[0]    
        except socket.herror:
            hostname = "Unable to retrieve hostname"
        self.hosts[ip] = hostname    
        return hostname
    
    def enumerate_hosts(self):
        addresses = self.get_network_addresses()
        threads = []
        for address in addresses:
            print(address)
            thread = Thread(target=self.ip_to_hostname, args=(address, ))
            threads.append(thread)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        

class Host(object):
    def __init__(self, name, address) -> None:
        self.name = name
        self.address = address
    

class MacAddress(object):
    def __init__(self, mac_or_ip: str=None) -> None:
        """Representation of a mac address, will validate the address or take an ipaddress and convert it to a mac address

        Args:
            mac_or_ip (str, optional): mac address or a ipaddress string. Defaults to None.
        """
        # determine if it is a mac address or an ip address
        self.value = mac_or_ip
        self.length = len(mac_or_ip)
        self.is_valid = self._validate()
        self._from_ipaddress()
    
    def _from_ipaddress(self):
        if self.is_valid == False:
            command = "arp -a {}".format(self.value)
            output = subprocess.check_output(command, shell=True).decode()
            mac_address = None
            for line in output.splitlines():
                if self.value in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        mac_address = parts[1].replace("-", ":")
            self.value = mac_address
    
    def _validate(self):
        pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
        if re.match(pattern, self.value):
            return True
        else:
            return False
    
    def __str__(self):
        return self.value
    
    def get(self):
        return self.value