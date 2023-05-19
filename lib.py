from dataclasses import dataclass
import subprocess


@dataclass(slots=True)
class ButtonText:
    fast_forward = "▶▶"
    play = "▶"
    rewind = "◀◀"
    left = "⇦"
    right = "⇨"
    up = "⇧"
    down = "⇩"
    channel_up = "CH ⇧"
    channel_down = "CH ⇩"
    volume_up = "Vol ⇧"
    volume_down = "Vol ⇩"
    mute = "Mute"

html_colors = [
    "AliceBlue", "AntiqueWhite", "Aqua", "Aquamarine", "Azure", "Beige", "Bisque", "Black", "BlanchedAlmond", "Blue",
    "BlueViolet", "Brown", "BurlyWood", "CadetBlue", "Chartreuse", "Chocolate", "Coral", "CornflowerBlue",
    "Cornsilk", "Crimson", "Cyan", "DarkBlue", "DarkCyan", "DarkGoldenRod", "DarkGray", "DarkGrey", "DarkGreen",
    "DarkKhaki", "DarkMagenta", "DarkOliveGreen", "DarkOrange", "DarkOrchid", "DarkRed", "DarkSalmon",
    "DarkSeaGreen", "DarkSlateBlue", "DarkSlateGray", "DarkSlateGrey", "DarkTurquoise", "DarkViolet", "DeepPink",
    "DeepSkyBlue", "DimGray", "DimGrey", "DodgerBlue", "FireBrick", "FloralWhite", "ForestGreen", "Fuchsia",
    "Gainsboro", "GhostWhite", "Gold", "GoldenRod", "Gray", "Grey", "Green", "GreenYellow", "HoneyDew", "HotPink",
    "IndianRed", "Indigo", "Ivory", "Khaki", "Lavender", "LavenderBlush", "LawnGreen", "LemonChiffon", "LightBlue",
    "LightCoral", "LightCyan", "LightGoldenRodYellow", "LightGray", "LightGrey", "LightGreen", "LightPink",
    "LightSalmon", "LightSeaGreen", "LightSkyBlue", "LightSlateGray", "LightSlateGrey", "LightSteelBlue",
    "LightYellow", "Lime", "LimeGreen", "Linen", "Magenta", "Maroon", "MediumAquaMarine", "MediumBlue",
    "MediumOrchid", "MediumPurple", "MediumSeaGreen", "MediumSlateBlue", "MediumSpringGreen", "MediumTurquoise",
    "MediumVioletRed", "MidnightBlue", "MintCream", "MistyRose", "Moccasin", "NavajoWhite", "Navy", "OldLace",
    "Olive", "OliveDrab", "Orange", "OrangeRed", "Orchid", "PaleGoldenRod", "PaleGreen", "PaleTurquoise",
    "PaleVioletRed", "PapayaWhip", "PeachPuff", "Peru", "Pink", "Plum", "PowderBlue", "Purple", "RebeccaPurple",
    "Red", "RosyBrown", "RoyalBlue", "SaddleBrown", "Salmon", "SandyBrown", "SeaGreen", "SeaShell", "Sienna",
    "Silver", "SkyBlue", "SlateBlue", "SlateGray", "SlateGrey", "Snow", "SpringGreen", "SteelBlue", "Tan",
    "Teal", "Thistle", "Tomato", "Turquoise", "Violet", "Wheat", "White", "WhiteSmoke", "Yellow", "YellowGreen"
]
    
@dataclass(slots=True)
class Arrow:
    left = "⇦"
    right = "⇨"
    up = "⇧"
    down = "⇩"
    
@dataclass(slots=True)
class Keypress:
    right = "/keypress/Right"
    left = "/keypress/Left"
    up = "/keypress/Up"
    down = "/keypress/Down"
    home = "/keypress/Home"
    select = "/keypress/Select"
    back = "/keypress/Back"
    repeat = "/keypress/InstantReplay"
    info = "/keypress/Info"
    rewind = "/keypress/Rev"
    forward = "/keypress/Fwd"
    play = "/keypress/Play"
    backspace = "/keypress/Backspace"
    search = "/keypress/Search"
    enter = "/keypress/Enter"

@dataclass(slots=True)
class Channel:
    down = "/ChannelDown"
    up = "/ChannelUp"

@dataclass(slots=True)
class Volume:
    down = "/keypress/VolumeDown"
    up = "/keypress/VolumeUp"
    mute = "/keypress/VolumeMute"

@dataclass(slots=True)
class Power:
    off = "/keypress/PowerOff"
    on = "/keypress/PowerOn"

@dataclass(slots=True)
class Input:
    tuner = "/InputTuner"
    hdmi1 = "/InputHDMI1"
    hdmi2 = "/InputHDMI2"
    hdmi3 = "/InputHDMI3"
    hdmi4 = "/InputHDMI4"
    avi = "/InputAV1"    

@dataclass(slots=True)
class Find:
    remote = "/FindRemote"

@dataclass(slots=True)
class Query:
    userinfo = "/query/registry/dev?s=UserInfo|UserId"
    tv_channels = "/query/tv-channels"
    active_channel = "/query/tv-active-channel"
    track_beacons = "/fwbeacons/track"
    untrack_beacons = "/fwbeacons/untrack"
    beacons = "/query/fwbeacons"
    chan_registry = "/query/registy" # requires channel name and stuff
    revents = "/query/sgrendezvous"
    stop_tracking = "/query/sgrendezvous/untrack"
    start_tracking = "/query/sgrendezvous/track"
    info = "/query/device-info"
    media_player = "/query/media-player"
    channel_performance = "/query/channel-perf"
    texture_memory = "/query/r2d2-bitmaps"
    channel_nodes = "/query/sgnodes/all"
    all_nodes = "/query/sgnodes/roots"


charcode_map = {
    'Backspace': 8, 'Tab': 9, 'Enter': 13, 'Shift': 16, 'Ctrl': 17, 'Alt': 18, 'Pause': 19, 'Caps Lock': 20, 'Esc': 27, 
    'Space': 32, 'Page Up': 33, 'Page Down': 34, 'End': 35, 'Home': 36, 'Left Arrow': 37, 'Up Arrow': 38, 'Right Arrow': 39, 
    'Down Arrow': 40, 'Insert': 45, 'Delete': 46, '0': 48, '1': 49, '2': 50, '3': 51, '4': 52, '5': 53, '6': 54, '7': 55, '8': 56, 
    '9': 57, 'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70, 'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76, 'M': 77, 
    'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82, 'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88, 'Y': 89, 'Z': 90, 
    'Left Windows Key': 91, 'Right Windows Key': 92, 'Menu': 93, 'Numpad 0': 96, 'Numpad 1': 97, 'Numpad 2': 98, 'Numpad 3': 99, 
    'Numpad 4': 100, 'Numpad 5': 101, 'Numpad 6': 102, 'Numpad 7': 103, 'Numpad 8': 104, 'Numpad 9': 105, 'Numpad *': 106, 
    'Numpad +': 107, 'Numpad -': 109, 'Numpad .': 110, 'Numpad /': 111, 'F1': 112, 'F2': 113, 'F3': 114, 'F4': 115, 'F5': 116, 
    'F6': 117, 'F7': 118, 'F8': 119, 'F9': 120, 'F10': 121, 'F11': 122, 'F12': 123, 'Num Lock': 144, 'Scroll Lock': 145, ';': 186, 
    '=': 187, ',': 188, '-': 189, '.': 190, '/': 191, '`': 223, '[': 219, '\\': 220, ']': 221, "'": 222}

keycode_map = {
    '8': 'Backspace',
    '9': 'Tab',
    '13': 'Enter',
    '16': 'Shift',
    '17': 'Ctrl',
    '18': 'Alt',
    '19': 'Pause',
    '20': 'Caps Lock',
    '27': 'Esc',
    '32': 'Space',
    '33': 'Page Up',
    '34': 'Page Down',
    '35': 'End',
    '36': 'Home',
    '37': 'Left Arrow',
    '38': 'Up Arrow',
    '39': 'Right Arrow',
    '40': 'Down Arrow',
    '45': 'Insert',
    '46': 'Delete',
    '48': '0',
    '49': '1',
    '50': '2',
    '51': '3',
    '52': '4',
    '53': '5',
    '54': '6',
    '55': '7',
    '56': '8',
    '57': '9',
    '65': 'A',
    '66': 'B',
    '67': 'C',
    '68': 'D',
    '69': 'E',
    '70': 'F',
    '71': 'G',
    '72': 'H',
    '73': 'I',
    '74': 'J',
    '75': 'K',
    '76': 'L',
    '77': 'M',
    '78': 'N',
    '79': 'O',
    '80': 'P',
    '81': 'Q',
    '82': 'R',
    '83': 'S',
    '84': 'T',
    '85': 'U',
    '86': 'V',
    '87': 'W',
    '88': 'X',
    '89': 'Y',
    '90': 'Z',
    '91': 'Left Windows Key',
    '92': 'Right Windows Key',
    '93': 'Menu',
    '96': 'Numpad 0',
    '97': 'Numpad 1',
    '98': 'Numpad 2',
    '99': 'Numpad 3',
    '100': 'Numpad 4',
    '101': 'Numpad 5',
    '102': 'Numpad 6',
    '103': 'Numpad 7',
    '104': 'Numpad 8',
    '105': 'Numpad 9',
    '106': 'Numpad *',
    '107': 'Numpad +',
    '109': 'Numpad -',
    '110': 'Numpad .',
    '111': 'Numpad /',
    '112': 'F1',
    '113': 'F2',
    '114': 'F3',
    '115': 'F4',
    '116': 'F5',
    '117': 'F6',
    '118': 'F7',
    '119': 'F8',
    '120': 'F9',
    '121': 'F10',
    '122': 'F11',
    '123': 'F12',
    '144': 'Num Lock',
    '145': 'Scroll Lock',
    '186': ';',
    '187': '=',
    '188': ',',
    '189': '-',
    '190': '.',
    '191': '/',
    '192': '`',
    '219': '[',
    '220': '\\',
    '221': ']',
    '222': "'",
    '223': '`',
    }

keys = list(charcode_map.keys())
keycodes = list(charcode_map.values())

def to_key(char):
    return charcode_map[char]

def to_char(keycode):
    key = str(keycode)
    return keycode_map[key]



def ping_device(device_ip) -> bool|None:
    try:
        # Run the ping command as a subprocess
        ping_process = subprocess.Popen(['ping', '-c', '4', device_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for the process to complete without blocking the main thread
        ping_process.wait()
        # Read the output and error streams
        output = ping_process.stdout.read().decode('utf-8')
        if ping_process.returncode == 0:
            return True
        else:
            return False
    except Exception as e:
        return None


