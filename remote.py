import requests
import time
from lib import Keypress, Channel, Volume, Power, Input, Find, Query

    
class RokuRemoteHeader:
    KEY_connection = "Connection"
    KEY_content_length = "Content-Length"
    KEY_accept = "Accept"
    KEY_user_agent = "User-Agent"
    KEY_accept_encoding = "Accept-Encoding"
    KEY_accept_language = "Accept-Language"
    keys = (
        KEY_connection, KEY_content_length, KEY_accept, KEY_user_agent, KEY_accept_encoding, KEY_accept_language
    )
    properties = ('')
    def __init__(self, connection: str= 'keep-alive', 
                 content_length:int=0, 
                 accept='application/json, text/plain, */*', 
                 user_agent: str="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) roku_remote_tool/4.0.5 Chrome/96.0.4664.55 Electron/16.0.5 Safari/537.36",
                 accept_encoding='gzip, deflate',
                 accept_language='en-US') -> None:
        self.connection = connection
        self.content_length = content_length
        self.accept = accept
        self.user_agent = user_agent 
        self.accept_encoding = accept_encoding
        self.accept_language = accept_language
        self.values = (self.connection, self.content_length, self.accept, self.user_agent, self.accept_encoding, self.accept_language)
        self.headers = {}
        for idx, item in enumerate(self.values):
            key = self.keys[idx]
            self.headers[key] = str(item)
    
    def get(self):
        return self.headers


class RokuRemote(object):
    
    def __init__(self, ip_address=None) -> None:
        self._address = ip_address
        self.name = None
        self.header_object = RokuRemoteHeader()
        self.headers  = self.header_object.get()
        self.address = f"http://{self._address}:8060"
        self.programmed = False if self._address is None else True
        self.combomap = {"home":self.home, "left":self.left, "right":self.right, "up":self.up, "down":self.down, "back":self.back, "forward":self.forward, "rewind":self.rewind, "play":self.play, "pause":self.play}
        self.buttons_pressed = 0
        self.response = None 


    def Address(self, value) -> None:
        self._address = value
        self.address = f"http://{self._address}:8060"
        self.programmed = False if self._address is None else True
    

    def Device(self) -> None:
        return self._address

    def get_device(self) -> None:
        return self.Device()
                
    def power(self):
        print("Power")
        url = self.address
        self.response = requests.post(url, headers=self.headers)
        self.buttons_pressed+=1
        
    def set_device(self, ip_address):
        self.Address(ip_address)
        
    def right(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.right
        self.response = requests.post(url, headers=self.headers)
        
    def left(self):
        self.buttons_pressed+=1
        print("Left")
        url = self.address + Keypress.left
        self.response = requests.post(url, headers=self.headers)
    
    def up(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.up
        self.response = requests.post(url, headers=self.headers)
    
    def down(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.down
        self.response = requests.post(url, headers=self.headers)
    
    def home(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.home
        self.response = requests.post(url, headers=self.headers)
        
    def info(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.info
        self.response = requests.post(url, headers=self.headers)
    
    def back(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.back
        self.response = requests.post(url, headers=self.headers)
    
    def play(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.play
        self.response = requests.post(url, headers=self.headers)
    
    def forward(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.forward
        self.response = requests.post(url, headers=self.headers)
    
    def rewind(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.rewind
        self.response = requests.post(url, headers=self.headers)
        
    def select(self):
        self.buttons_pressed+=1
        url = self.address + Keypress.select
        self.response = requests.post(url, headers=self.headers)
    
    def touch_screen(self, x: float, y: float):
        url = self.address + f"/input?touch.0.x={x}&touch.0.y={y}&touch.0.op=down"
        self.response = requests.post(url, headers=self.headers)
        
    def volume_up(self):
        self.buttons_pressed+=1
        url = self.address + Volume.up 
        ressponse = requests.post(url, headers=self.headers)
    
    def volume_down(self):
        self.buttons_pressed+=1
        url = self.address + Volume.down 
        self.response = requests.post(url, headers=self.headers)
    
    def mute(self):
        self.buttons_pressed+=1
        url = self.address + Volume.mute 
        self.response = requests.post(url, headers=self.headers)
    
    def channel_up(self):
        self.buttons_pressed+=1
        url = self.address + Channel.up 
        self.response = requests.post(url, headers=self.headers)
    
    def channel_down(self):
        self.buttons_pressed+=1
        url = self.address + Channel.down 
        self.response = requests.post(url, headers=self.headers)
    
    def combo(self, combo):
        for c in combo:
            self.combomap[c]()
            time.sleep(0.15)
            
    
    def enable_dev_mode(self):
        for i in range(3):
            self.home()
            time.sleep(0.15)
        for i in range(2):
            self.up()
            time.sleep(0.15)
        for i in range(2):
            self.left()
            time.sleep(0.15)
            self.right()
            time.sleep(0.15)
        self.left()
    
    def network_info(self):
        self.combo(["home", "home", "home", "home", "home", "right", "left", "right", "left", "right"])
    
    def platform_details(self):
        self.combo(["home", "home", "home", "home", "home", "forward", "play", "rewind", "play", "forward"])
    
    def reset_and_update(self):
        self.combo(["home", "home", "home", "home", "home", "forward","forward","forward", "rewind","rewind"])
    
    def assests(self):
        self.combo(["home", "home", "home", "home", "home", "up", "right", "down", "left", "up"])
    
    def wireless_details(self):
        self.combo(["home", "home", "home", "home", "home", "up", "down", "up","down", "up"])
    
    def reboot(self):
        self.combo(["home", "home", "home", "home", "home", "up", "rewind", "rewind", "forward", "forward"])

