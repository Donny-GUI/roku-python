
print("init")
import customtkinter as ctk
from remote import RokuRemote
from threading import Thread
import socket
from lib import ButtonText, Arrow
from lib import to_char, to_key, keys, keycodes, ping_device
import subprocess
import os
import atexit
from pprint import pprint


CWD = os.getcwd()
NETENUM_EXE = os.path.join(CWD, "network_enumerator.exe")
NETENUM_PY = os.path.join(CWD, "network_enumerator.py")
CMD = f"python {NETENUM_PY}"

class RokuRemoteApp(ctk.CTk):
    
    def __init__(self) -> None:
        print("loading")
        super().__init__()
        self.network = {}
        #self.read_files()
        #self.network_enumerator = subprocess.Popen([CMD], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        #self.network_enumerator = subprocess.Popen([NETENUM_EXE], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        atexit.register(self.cleanup)
        
        self.remote = RokuRemote("192.168.50.166")
        self.devices = []
        self.addresses = []
        self.Keys = []
        self.add_device(self.remote._address)

        self.max_width = 275
        self.geometry(f"210x650")
        
        self.first_check = ping_device(self.remote._address)
        self.status = "Loading..."
        
        # outer frame
        self.outer_frame = ctk.CTkFrame(self, width=273)
        self.outer_frame.grid(row=1, column=0, pady=2, padx=0, ipadx=2, sticky='W')
        
        self.bind("<Key>", self.key_pressed)
        
        # power frame
        self.power_frame = ctk.CTkFrame(self.outer_frame)
        self.power_frame.grid(row=0, column=0, pady=5, padx=(0,0), sticky='WE')
        
        # navigation frame
        self.navigation_frame = ctk.CTkFrame(self.outer_frame, border_width=5)
        self.navigation_frame.grid(row=1, column=0, pady=5, padx=7, sticky='W')
        
        # updown frame
        self.updown_frame = ctk.CTkFrame(self.outer_frame, border_width=5)
        self.updown_frame.grid(row=2, column=0, pady=5, padx=0, sticky='W')
        
        # channel updown frame
        self.updown_channel_frame = ctk.CTkFrame(self.updown_frame)
        self.updown_channel_frame.grid(row=0, column=0, padx=(32,5), pady=(5,5), sticky='W')
        
        
        # volume updown frame
        self.updown_volume_frame = ctk.CTkFrame(self.updown_frame)
        self.updown_volume_frame.grid(row=0, column=2, padx=(5,35), pady=(5,5), sticky='E')
        
        # mute frame
        self.mute_frame = ctk.CTkFrame(self.updown_frame)
        self.mute_frame.grid(row=0, column=1)
        
        # control frame
        self.control_frame = ctk.CTkFrame(self.outer_frame)
        self.control_frame.grid(row=3, column=0, pady=5, padx=(35,5), sticky='w')
        
        # address frame
        self.address_frame = ctk.CTkFrame(self.outer_frame)
        self.address_frame.grid(row=4, column=0, pady=5, padx=5, sticky='W')
        
        # set address frame
        self.set_address_frame = ctk.CTkFrame(self.address_frame)
        self.set_address_frame.grid(row=2, column=0, pady=5, padx=(10,10))
        
        # extra buttons frame
        self.extra_buttons_frame = ctk.CTkFrame(self.outer_frame, border_width=5, border_color='tomato')
        self.extra_buttons_frame.grid(row=5, column=0, pady=5, padx=5, sticky='W')
        self.extra_buttons_frame.grid_forget()
        
        # status frame
        self.status_frame = ctk.CTkFrame(self.outer_frame, border_width=5, border_color='slategray', bg_color='black', fg_color='black')
        self.status_frame.grid(row=6, column=0, pady=5, padx=5, sticky='W')
        
        # statusbox
        self.status_box = ctk.CTkTextbox(self.status_frame, bg_color='green', fg_color='black', width=200, height=200, text_color="green")
        self.status_box.grid(row=0, column=0, sticky="WESN")
        self.status_box_x = 0 
        self.status_box_y = 0
        self.message_box_width = 30 
        
        # power button
        self.power_button = ctk.CTkButton(self.power_frame, text="Power", width=35, fg_color="red")
        self.power_button.grid(row=0, column=0, pady=5, padx=0, sticky='w')
        self.power_button.bind("<Button-1>", self.wake_up)

        # devices combo box
        self.device_combo_box = ctk.CTkComboBox(self.power_frame, values=self.devices)
        self.device_combo_box.grid(row=0, column=1, pady=5, padx=(10,5), sticky='e')
        self.device_combo_box.bind("<<ComboBoxSelected>>", self.device_selected_from_combo)
        
        # [  Volume Buttons   ]

        # vol down button
        self.volume_down_button = ctk.CTkButton(self.updown_volume_frame, text=ButtonText.volume_down, width=25)
        self.volume_down_button.grid(row=1, column=0, sticky='W', pady=(1,1))
        self.volume_down_button.bind("<Button-1>", lambda event_release: self.remote.volume_down())
        self.volume_down_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("volume_down_button"))

        # vol up button
        self.volume_up_button = ctk.CTkButton(self.updown_volume_frame, text=ButtonText.volume_up, width=25)
        self.volume_up_button.grid(row=0, column=0, sticky='W', pady=(1,1))
        self.volume_up_button.bind("<Button-1>", lambda event_release: self.remote.volume_up())
        self.volume_up_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("volume_up_button"))

        # vol mute button
        self.mute_button = ctk.CTkButton(self.mute_frame, text=ButtonText.mute, width=25)
        self.mute_button.grid(row=0, column=0, sticky='W')
        self.mute_button.bind("<Button-1>", lambda event_release: self.remote.mute())
        
        
        # [ Channel Buttons     ]
        
        # ch up button 
        self.channel_up_button = ctk.CTkButton(self.updown_channel_frame, text=ButtonText.channel_up, width=25)
        self.channel_up_button.grid(row=0, column=0, pady=(1,1), sticky='W')
        
        # ch down button
        self.channel_down_button = ctk.CTkButton(self.updown_channel_frame, text=ButtonText.channel_down, width=25)
        self.channel_down_button.grid(row=1, column=0, pady=(1,1), sticky='W')
        
        
        # Navigation buttons
        
        # up button
        self.up_button = ctk.CTkButton(self.navigation_frame, text=Arrow.up, width=45, border_width=1)
        self.up_button.bind("<Button-1>", lambda event_release: self.remote.up())
        self.up_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("up_button"))
        self.up_button.grid(row=1, column=1, pady=5, padx=5)
        
        # left button
        self.left_button = ctk.CTkButton(self.navigation_frame, text=Arrow.left, width=45, border_width=1)
        self.left_button.bind("<Button-1>", lambda event_release: self.remote.left())
        self.left_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("left_button"))
        self.left_button.grid(row=2, column=0, pady=5, padx=5)
        
        # ok button
        self.ok_button = ctk.CTkButton(self.navigation_frame, text="Select", width=45, fg_color="green")
        self.ok_button.bind("<Button-1>", lambda event_release: self.remote.select())
        self.ok_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("ok_button"))
        self.ok_button.grid(row=2, column=1, pady=5, padx=5)
        
        # right button
        self.right_button = ctk.CTkButton(self.navigation_frame, text=Arrow.right, width=45, border_width=1)
        self.right_button.bind("<Button-1>", lambda event_release: self.remote.right())
        self.right_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("right_button"))
        self.right_button.grid(row=2, column=2, pady=5, padx=5)
        
        # down button
        self.down_button = ctk.CTkButton(self.navigation_frame, text=Arrow.down, width=45, border_width=1)
        self.down_button.bind("<Button-1>", lambda event_release: self.remote.down())
        self.down_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("down_button"))
        self.down_button.grid(row=3, column=1, pady=5, padx=5)

        # [ Control buttons ]
        
        # back button
        self.back_button = ctk.CTkButton(self.navigation_frame, text="☚Back", width=45)
        self.back_button.bind("<Button-1>", lambda event_release: self.remote.back())
        self.back_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("back_button"))
        self.back_button.grid(row=4, column=0, pady=5, padx=5)
        
        # home button
        self.home_button = ctk.CTkButton(self.navigation_frame, text="🏠Home", width=45, fg_color="purple")
        self.home_button.bind("<Button-1>", lambda event_release: self.remote.home())
        self.home_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("home_button"))
        self.home_button.grid(row=4, column=2, pady=5, padx=5)
        
        # info button
        self.info_button = ctk.CTkButton(self.control_frame, text="Info", width=45, border_width=1)
        self.info_button.bind("<Button-1>", lambda event_release: self.remote.info())
        self.info_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("info_button"))
        self.info_button.grid(row=0, column=1, pady=5, padx=0)
        
        # fast forward button
        self.fwd_button = ctk.CTkButton(self.control_frame, text="▶▶", width=45)
        self.fwd_button.bind("<Button-1>", lambda event_release: self.remote.forward())
        self.fwd_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("fwd_button"))
        self.fwd_button.grid(row=1, column=2, pady=5, padx=0)
        
        # play button
        self.play_button = ctk.CTkButton(self.control_frame, text="▶", width=45)
        self.play_button.bind("<Button-1>", lambda event_release: self.remote.play())
        self.play_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("play_button"))
        self.play_button.grid(row=1, column=1, pady=5, padx=0)
        
        # rewind button
        self.rwd_button = ctk.CTkButton(self.control_frame, text="◀◀", width=45)
        self.rwd_button.bind("<Button-1>", lambda event_release: self.remote.rewind())
        self.rwd_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("rwd_button"))
        self.rwd_button.grid(row=1, column=0, pady=5, padx=0)
        
        # address set button
        self.address_button = ctk.CTkButton(self.set_address_frame, text="set", width=50)
        self.address_button.bind("<Button-1>", lambda event_release: self.get_address_set_device())
        self.address_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("address_button"))
        self.address_button.grid(row=2, column=0, pady=5, padx=(10,5), sticky='W')
        
        # address entry box
        self.address_box = ctk.CTkEntry(self.set_address_frame,  width=100)
        self.basic_address = "192.168.50."
        for index, i in enumerate(self.basic_address):
            self.address_box.insert(index, i)
        self.address_box.grid(row=2, column=1, padx=(5,10), pady=5, sticky='W')
        
        # active dev mode button
        self.active_devmode_button = ctk.CTkButton(self.extra_buttons_frame, text="Activate Dev Mode")
        self.active_devmode_button.bind("<Button-1>", lambda event_release: self.remote.enable_dev_mode())
        self.active_devmode_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("active_devmode_button"))
        self.active_devmode_button.grid(row=0, column=0, pady=5, padx=0, ipadx=0,sticky='W')
        self.active_devmode_button.grid_forget()
        
        # network button 
        self.network_button = ctk.CTkButton(self.extra_buttons_frame, text="Network Info")
        self.network_button.bind("<Button-1>", lambda event_release: self.remote.network_info())
        self.network_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("network_button"))
        self.network_button.grid(row=1, column=0, pady=5, padx=0, ipadx=0,sticky='W')
        self.network_button.grid_forget()
        
        # platform details button 
        self.platform_details_button = ctk.CTkButton(self.extra_buttons_frame, text="Platform Details")
        self.platform_details_button.bind("<Button-1>", lambda event_release: self.remote.platform_details())
        self.platform_details_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("platform_details_button"))
        self.platform_details_button.grid(row=2, column=0, pady=5, padx=0, ipadx=0,sticky='W')
        self.platform_details_button.grid_forget()
        
        # reset and update button 
        self.platform_details_button = ctk.CTkButton(self.extra_buttons_frame, text="Reset and Update TV")
        self.platform_details_button.bind("<Button-1>", lambda event_release: self.remote.platform_details())
        self.platform_details_button.bind("<Button-1>", lambda event: self.send_message_to_status_box("platform_details_button"))
        self.platform_details_button.grid(row=3, column=0, pady=5, padx=0, ipadx=0,sticky='W')
        self.platform_details_button.grid_forget()
        
        # setup the textbox
        self.status_box.insert("0.0", "➱")
        
        self.after(0, self.send_message_to_status_box("Remote Initialized"))
        
        if self.first_check == True:
            self.after(100, self.send_message_to_status_box(f"{self.remote._address} Connected"))
            self.status = 'connected'
        elif self.first_check == False:
            self.after(100, self.send_message_to_status_box(f"[ ! ][ Roku Unresponsive"))
            self.status = 'disconnected'
        elif self.first_check == None:
            self.after(100, self.send_message_to_status_box(f"[ ! ][Roku address error"))
            self.status = 'disconnected'
        
        # key bindings set
        self.bindings = {}
        for char in keys:
            self.bindings[char] = None
        self.bindings["Left Arrow"] = self.remote.left 
        self.bindings["Right Arrow"] = self.remote.right
        self.bindings["Up Arrow"] = self.remote.up
        self.bindings["Down Arrow"] = self.remote.down
        self.bindings["Space"] = self.remote.select

        self.read_files()
        self.mainloop()

    def cleanup(self):
        self.network_enumerator.terminate()
    
    def read_files(self):
        files = [x for x in os.listdir(CWD) if x.startswith("network_addresses")]
        paths = [os.path.join(CWD, x) for x in files]
        for path in paths:
            with open(path, 'r') as rfile:
                lines = rfile.readlines()
            for line in lines:
                addr, name = line.split("\t")
                na = name.strip("\n")
                self.network[addr] = na
            os.remove(path)
        pprint(self.network)
        self.after(5000, self.enumerate_network)
        self.after(10000, self.read_files)
    
    def enumerate_network(self):
        self.network_enumerator = subprocess.Popen([NETENUM_EXE], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        
    def remove_files(self):
        files = [x for x in os.listdir(CWD) if x.startswith("network_addresses")]
        paths = [os.path.join(CWD, x) for x in files]
        for path in paths:
            os.remove(path)
        
    def device_selected_from_combo(self, event):
        selected_item = self.device_combo_box.get()
        self.remote.set_device(selected_item)
    
    def send_message_to_status_box(self, message):
        thread = Thread(target=self._send_message_to_status_box, args=(message,))
        self.status_box.after_idle(thread.run)
    
    def _send_message_to_status_box(self, message):
        self.status_box.configure(state="normal")
        # remove arrow from last line
        self.status_box.delete(f"{self.status_box_y}.0")
        # go to next line
        self.status_box_y+=1
        # add arrow and endline
        message = "➱" + message + "\n"
        mlength = len(message)
        mcount = -1
        # insert each character in their slot
        for char in message:
            mcount += 1
            if mlength == mcount:
                mcount = -1
                self.status_box_y += 1
            pos = f"{self.status_box_y}.{mcount}"
            self.status_box.insert(pos, char)
        self.status_box.configure(state='disabled')
        
    def add_device(self, device_ip: str) -> None:
        if device_ip not in self.devices:
            self.devices.append(device_ip)
        address = f"https://{device_ip}:8086"
        self.addresses.append(address)
        
    def set_address_box(self, text):
        """ sets the address box default value """
        current = self.address_box.get()
        for index, i in enumerate(current):
            self.address_box.delete(index)
        for index, char in enumerate(text):
            self.address_box.insert(index, char)   

    def get_address_set_device(self):
        address = self.address_box.get()
        self.remote.set_device(address)
    
    def wake_up(self, mac_address):
        """takes the remote address and gets the mac address of the device, 
        then creates a magic packet and sends it to the network
        """
    
        mac_parts = self.mac_address.split(":")
        mac_bytes = [int(part, 16) for part in mac_parts]
        magic_packet = b'\xFF' * 6 + (b''.join(mac_bytes) * 16)
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.sendto(magic_packet, ('<broadcast>', 9))
    
    def key_pressed(self, key):
        char = to_char(key.keycode)
        print(char)
        function = self.bindings[char]
        print(function)
        if function is not None:
            function()

if __name__ == '__main__':
    print("main")
    remote = RokuRemoteApp()

