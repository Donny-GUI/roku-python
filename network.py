
import subprocess
import re
import socket
import os
from dataclasses import dataclass
from typing import Iterable
import os
import requests
import asyncio
import socket
import struct


def send_wake_on_lan(mac_address):
    
    # Create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set up the destination address and port
    # Use the broadcast address to send the packet to all devices in the local network
    dest_address = ('<broadcast>', 9)

    # Construct the magic packet
    mac_bytes = mac_address.replace(':', '').decode('hex')
    magic_packet = b'\xff' * 6 + mac_bytes * 16

    # Send the magic packet to the destination address
    s.sendto(magic_packet, dest_address)

    # Close the socket
    s.close()

@dataclass(slots=True)
class Pair:
    host: str
    port: int

    
class InternetFamily:
    four = socket.AF_INET
    six = socket.AF_INET6
    bluetooth = socket.AF_BLUETOOTH
    appletalk = socket.AF_APPLETALK
    internetwork_packet_exchange = socket.AF_IPX
    digital_equipment_corp = socket.AF_DECnet
    infared_data = socket.AF_IRDA
    link_layer = socket.AF_LINK
    systems_network_architecture = socket.AF_SNA
    unspecific = socket.AF_UNSPEC

class Protocol:
    layer_2_tunneling = socket.IPPROTO_L2TP
    authentication_header = socket.IPPROTO_AH
    options = socket.IPPROTO_IP
    internet_control_message = socket.IPPROTO_ICMP
    internet_control_message_6 = socket.IPPROTO_ICMPV6
    internet_group_management = socket.IPPROTO_IGMP
    gateway_to_gateway = socket.IPPROTO_GGP
    ipv4_encapsulation = socket.IPPROTO_IPV4
    ipv6_encapsulation = socket.IPPROTO_IPV6
    stream = socket.IPPROTO_ST
    transmission_control = socket.IPPROTO_TCP
    core_based_trees = socket.IPPROTO_CBT
    exterior_gateway = socket.IPPROTO_EGP
    private_interior = socket.IPPROTO_EGP
    parc_universal_pack = socket.IPPROTO_PUP
    user_datagram = socket.IPPROTO_UDP 
    internet_datagram = socket.IPPROTO_IDP
    reliable_data = socket.IPPROTO_RDP
    net_disk = socket.IPPROTO_ND
    wideband_monitoring = socket.IPPROTO_ICLFXBM
    independent_multicast = socket.IPPROTO_PIM 
    pragmatic_general_multicast = socket.IPPROTO_PGM 
    stream_control_transmission = socket.IPPROTO_SCTP
    raw_ip_packets = socket.IPPROTO_RAW
    

class Socket:
    stream = socket.SOCK_STREAM
    datagram = socket.SOCK_DGRAM
    raw = socket.SOCK_RAW
    sequential_packet = socket.SOCK_SEQPACKET
    reliable_datagram = socket.SOCK_RDM

class BluetoothProtocol:
    radio_comm = socket.BTPROTO_RFCOMM




#////////////////////////////////////////
# TCP
#////////////////////////////////////////

class TCPSocket(socket.socket):
    def __init__(self, internet_protocol=InternetFamily.four, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(internet_protocol, socket.SOCK_STREAM, proto, fileno)


class TCPListenSocket(TCPSocket):
    def __init__(self, address: str, port: int=8080, queue_connections=1, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(proto, fileno)
        self.address = address
        self.port = port
        self.queue_connections = queue_connections
        self.bind((self.address, self.port))
        self.listen(self.queue_connections)


class NonBlockingTCPSocket(TCPSocket):
    def __init__(self, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(proto, fileno)
        self.setblocking(False)

class TCPDatagramSocket(socket.socket):
    def __init__(self, family = InternetFamily.four, type:int = -1, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(family, socket.SOCK_DGRAM, proto, fileno)
        

#////////////////////////////////////////
# UCP
#////////////////////////////////////////

class UDPSocket(socket.socket):
    def __init__(self, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_DGRAM, proto, fileno)


class UDPListenSocket(UDPSocket):
    def __init__(self,address: str, port:int=8888, queued_connections:int=1, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(proto, fileno)
        self.address = address
        self.port = port
        self.queued_connections = queued_connections
        self.bind((self.address, self.port))
        self.listen(self.queued_connections)
        

class NonBlockingUDPSocket(UDPSocket):
    def __init__(self, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(proto, fileno)
        self.setblocking(False)


#////////////////////////////////////////
# RAW
#////////////////////////////////////////

class RawSocket(socket.socket):
    def __init__(self, proto: int = -1, fileno: int | None = None) -> None:
        super().__init__(socket.AF_INET, socket.SOCK_RAW, proto, fileno)


#////////////////////////////////////////
# BLUETOOTH
#////////////////////////////////////////


def pinga(ip_address: str):
    cmd = ["ping", "-a", ip_address]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = proc.communicate()
    output.decode()
    return output.split("\n")[0].split(" ")[1].strip()

class BluetoothSocket(socket.socket):
    macpattern = r"\b\w\w-\w\w-\w\w-\w\w-\w\w-\w\w\b"
    ip_address_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    def __init__(self, mac_address:str=None, port:int=1, fileno: int | None = None) -> None:


        super().__init__(InternetFamily.bluetooth, Socket.stream,  BluetoothProtocol.radio_comm)
        self.nmap = {}
        self.mac = mac_address
        self.port = port
        if self.mac is None:
            output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
            network_addresses = re.findall(self.ip_address_pattern, output)
            mac_addresses = re.findall(self.macpattern, output)
            hostnames = [socket.getfqdn(x) for x in network_addresses]
            self.nmap = {key:value for key, value in zip(hostnames, mac_addresses)}
            
            print(self.nmap)
            print(mac_addresses)
            print(network_addresses)
            print(hostnames)
            
btsock = BluetoothSocket()

exit()


class NetworkObject:
    def __str__(self):
        return self.address

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.address}')"


class IpAddress(NetworkObject):
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    
    def __init__(self, address: str) -> None:
        """ ip address class. will determine if it is you who is this address. 
        If the address is valid, the outward address for this ipaddress.
        If the address is on this network.
        if the address is active

        Args:
            address (str): _description_
        """
        # make the address formatted
        self.address: str = self.__format_address(address)
        # determine if it is a local ip
        self.local: bool = self.__is_local(self.address)
        # determing if it is reachable
        self.status: str = "inactive" # is this address active or reachable?
        # determine if it is a valid ip address
        self.valid: bool = False  
        # determine if this address is me
        self.me = self.__me()  # is this address me?
        
        self.validate()
        self.active()
        
        if self.valid:
            # if its valid address
            if self.__me:
                # if the valid address is me
                self.outward = requests.get('https://api.ipify.org?format=json')["ip"]
            else:
                self.outward = self.__get_outward()
        else:
            self.outward = None
    
    
    def __int__(self) -> int:
        return int(self.address.split(".")[-1])

    def __iter__(self) -> Iterable:
        return iter([int(x) for x in self.address.split(".")])
    
    def __is_local(self, address: str) -> bool:
        return IpAddress.local_address(address)
        
        
    
    def __me(self):
        """ Determines if the address is a reference to the current computer

        Returns:
            bool: False if not, True if so
        """
        plat = sys.platform
        hostname = socket.gethostname()
        if plat.startswith('linux') or plat.startswith('darwin'):
            # For Linux and macOS
            try:
                platform_hostname = platform.node()
            except:
                return False
            if hostname == platform_hostname:
                return True
            else:
                return False
                
        elif plat.startswith('win'):
            # For Windows
            try:
                platform_hostname = os.environ['COMPUTERNAME']
            except KeyError:
                return False
            finally:
                if hostname == platform_hostname:
                    return True
                else:
                    return True
        else:
            return False

    def __get_outward(self):
        
        if self.valid:
            # if its valid address
            if self.__me:
                # if the valid address is me
                self.outward = requests.get('https://api.ipify.org?format=json').json()["ip"]
            else:
                if IpAddress.local_address(self.address):
                    response = requests.get(f"http://{self.address}")
                    print(response)    
                
                
        else:
            self.outward = None


    def __format_address(self, address: str) -> None:
        address_parts = address.split(".")
        formatted_parts = [part.zfill(3) for part in address_parts]
        return ".".join(formatted_parts)
    
    
    @staticmethod
    async def async_is_active(address: str):
        if IpAddress.valid_address(address):
            if IpAddress.local_address(address):
                try:
                    output = subprocess.check_output(['ping', '-c', '1', '-W', '1', address])
                    return True
                except subprocess.CalledProcessError:
                    return False
            return False
                
        else:
            return False
    
    @staticmethod
    def is_active():
        pass
        
        
    

    @staticmethod
    def local_address(address: str) -> bool:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        
        checks = ".".join(address.split(".")[:-1])
        local_check = ".".join(ip.split(".")[:-1])
        
        if checks == local_check:
            return True
        else:
            return False
    
    @staticmethod 
    def find(str: str) -> list:
        return re.findall(IpAddress.pattern, str)
    
    @staticmethod
    def valid_address(ip_address: str) -> bool:
        truth = True
        address_parts = ip_address.split(".")
        
        if len(address_parts) != 4:
            truth = False
            return truth

        for part in address_parts:
            
            try:
                num = int(part)  
                if num < 0 or num > 255:
                    truth = False
                    break 
            
            except ValueError:
                truth = False
                break
        
        return truth

    async def validate(self) -> None:
        self.valid = True
        address_parts = self.address.split(".")
        if len(address_parts) != 4:
            self.valid = False

        for part in address_parts:
            try:
                num = int(part)
                if num < 0 or num > 255:
                    self.valid = False 
            except ValueError:
                self.valid = False

    def is_valid(self) -> bool:
        self.validate()
        return self.valid

    async def active(self) -> None:
        try:
            cmd = ['ping', '-c', '1', '-W', '1', self.address]
            proc = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            await proc.communicate()
            
            # Check if the process returned a zero exit code indicating a successful response
            if proc.returncode == 0:
                self.status = "active"
            else:
                self.status = "inactive"
        
        except subprocess.CalledProcessError:
            self.status = "inactive"

        


class MacAddress(NetworkObject):
    pattern = r'^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}$'
    def __init__(self, address: str) -> None:
        self.address = self.__format_address(address)
        self.validate()

    def __format_address(self, address):
        address = address.lower().replace("-", ":")
        address_parts = address.split(":")
        formatted_parts = [part.zfill(2) for part in address_parts]
        return ":".join(formatted_parts)

    def validate(self):
        address_parts = self.address.split(":")
        if len(address_parts) != 6:
            raise ValueError("Invalid MAC address")

        for part in address_parts:
            try:
                int(part, 16)
            except ValueError:
                raise ValueError("Invalid MAC address")

    def is_valid(self):
        try:
            self.validate()
            return True
        except ValueError:
            return False


class NetworkAddress:
    def __init__(self, ip_address: str, mac_address: str) -> None:
        self.ip = IpAddress(ip_address)
        self.mac = MacAddress(mac_address)

    def get(self):
        return {"ip": str(self.ip), "mac": str(self.mac)}

    def __str__(self):
        return f"IP: {str(self.ip)}, MAC: {str(self.mac)}"

    def __repr__(self):
        return f"NetworkAddress(ip_address='{str(self.ip)}', mac_address='{str(self.mac)}')"


class NetworkEnumerator:
    mac_address_pattern = r'^([0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}$'
    ip_address_pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    
    def __init__(self):
        self.output = subprocess.check_output(["arp", "-a"], universal_newlines=True)
        self.network_addresses = re.findall(self.ip_address_pattern, self.output)
        self.mac_addresses = re.findall(self.mac_address_pattern, self.output)
        self.addresses = []
        
    def enumerate_network_addresses(self):
        
        addresses = []
        network_index = 0
        current_address = self.network_addresses[network_index]
        end_address = self.network_addresses[-1]

        while current_address <= end_address:
            
            current_address = self.network_addresses[network_index]
            
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                sock.connect_ex((current_address, 80))
                hostname = socket.gethostbyaddr(str(current_address))[0]
                addresses.append((str(current_address), hostname))
            
            except socket.herror:
                addresses.append((str(current_address), "N/A"))

            network_index += 1
            
        names = os.listdir(os.getcwd())
        addrnames = [x for x in names if x.startswith("network_addresses")]
        fx = len(addrnames)
        f = "network_addresses" + str(fx)
        
        with open(f, "w") as wfile:
            
            for address in addresses:
                wfile.write(address[0]+ "\t"+ address[1] + "\n")
    

if __name__ == '__main__':
    ne = NetworkEnumerator()
    ne.enumerate_network_addresses()
