# -*- coding: utf-8 -*-

import json
import sys
import threading
import time
import win32api
import win32con
import winsound
import ctypes
from image_search import get_screen_area_as_image, load_image_from_file, search_image_in_image
from overlay_label import OverlayLabel
from keyboard_input import keyb_down, keyb_up


LMB = win32con.VK_LBUTTON
F4 = win32con.VK_F4
F10 = win32con.VK_F10
NUM_4 = win32con.VK_NUMPAD4
NUM_6 = win32con.VK_NUMPAD6
KEY_1 = 0x31
KEY_2 = 0x32
KEY_3 = 0x33
KEY_E = 0x45
KEY_R = 0x52

EMPTY_WEAPONS_LIST = [
    {
        "name": "None",
        "rpm": 6000,
        "check_image": None,
        "check_area": [1500, 950, 1735, 1030],
        "pattern": [
            [0,0],
        ]
    },
]

# for cursor detector
class POINT(ctypes.Structure):
    _fields_ = [('x', ctypes.c_int),
                ('y', ctypes.c_int)]

class CURSORINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint),
                ('flags', ctypes.c_uint),
                ('hCursor', ctypes.c_void_p),
                ('ptScreenPos', POINT)]

def beep_on():
    winsound.Beep(2000, 100)


def beep_off():
    winsound.Beep(1000, 100)


def beep_exit():
    winsound.Beep(500, 500)


def mouse_move_relative(dx, dy):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(dx), int(dy), 0, 0)


def lmb_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


def lmb_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


def rmb_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)


def rmb_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


def is_lmb_pressed():
    return win32api.GetKeyState(LMB) < 0


def cursor_detector():
    # Load and set argument types
    GetCursorInfo = ctypes.windll.user32.GetCursorInfo
    GetCursorInfo.argtypes = [ctypes.POINTER(CURSORINFO)]
    # Initialize the output structure
    info = CURSORINFO()
    info.cbSize = ctypes.sizeof(info)
    # Do it!
    if GetCursorInfo(ctypes.byref(info)):
        if info.flags & 0x00000001:
            return True
        else:
            return False
    else:
        print("WARNING: Cursor detector is not running!")
        

def load_weapons(weapon_filename):
    weapons_list = EMPTY_WEAPONS_LIST
    current_weapon_index = 0

    if not weapon_filename:
        print("WARNING: Filename with weapons data was not set! Meh!?")
        return weapons_list, current_weapon_index

    weapon_filepath = "./weapon_data/{}.json".format(weapon_filename)

    print("DEBUG: Trying to open and load data from {}".format(weapon_filepath))
    try:
        with open(weapon_filepath) as f:
            data = json.load(f)
            weapons_data = data["weapons"]
    except:
        print("ERROR: Can not open/read file with weapon data. No file? Corrupted? WTF!?")
        print("INFO: Since last error I will use default EMPTY_WEAPONS_LIST. Go check your data files, okay?")
        return weapons_list, current_weapon_index
    print("DEBUG: Not sure but looks like everything is okay :)")

    weapons_list = weapons_data

    for i, weapon in enumerate(weapons_list):
        if weapon["check_image"]:
            image = load_image_from_file("./weapon_data/{}_img\{}".format(weapon_filename, weapon["check_image"]))
            weapons_list[i]["image"] = image
        else:
            weapons_list[i]["image"] = None

    return weapons_list, current_weapon_index


def toggle_recoil(no_recoil):
    if no_recoil:
        beep_off()
    else:
        beep_on()
    return not no_recoil


def prev_weapon(weapons_list, current_weapon_index):
    if current_weapon_index < 1:
        current_weapon_index = len(weapons_list) - 1
    else:
        current_weapon_index -= 1
    return current_weapon_index


def next_weapon(weapons_list, current_weapon_index):
    if current_weapon_index > len(weapons_list) - 2:
        current_weapon_index = 0
    else:
        current_weapon_index += 1
    return current_weapon_index


def get_tick(rpm):
    rps = rpm/60
    mstick = 1000.0/rps
    stick = round(mstick/1000, 3)
    return stick


def construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil):
    recoil_data = "ON" if no_recoil else "OFF"
    bg_data = "#acffac" if no_recoil else "#ffacac"
    recoil_string = "NoRecoil: {}".format(recoil_data)
    weapon_string = "Weapon: {}".format(weapons_list[current_weapon_index]["name"])
    length = max(len(recoil_string), len(weapon_string))
    overlay_string = "{}\n{}".format(recoil_string.ljust(length), weapon_string.ljust(length))
    overlay.set_bg(bg_data)
    overlay.set_text(overlay_string)


def process_no_recoil(overlay, weapons_list, current_weapon_index, no_recoil):
    shot_index = 0
    shot_tick = get_tick(weapons_list[current_weapon_index]["rpm"])
    while is_lmb_pressed():
        current_pattern = weapons_list[current_weapon_index]["pattern"]
        if weapons_list[current_weapon_index]["name"] == "Peacekeeper":
            time.sleep(110 / 1000)
            lmb_up()
            keyb_down(KEY_R)
            time.sleep(110 / 1000)
            keyb_up(KEY_R)
            time.sleep(110 / 2000)
            keyb_down(KEY_3)
            time.sleep(110 / 2000)
            keyb_up(KEY_3)
            time.sleep(110 / 2000)
            keyb_down(KEY_2)
            time.sleep(100 / 2000)
            keyb_up(KEY_2)
            # time.sleep(750 / 2000)

        elif shot_index < len(current_pattern) - 1:
            dx = -current_pattern[shot_index][0]
            dy = -current_pattern[shot_index][1]
            mouse_move_relative(dx, dy)
            time.sleep(shot_tick)
            shot_index += 1
            construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil)


def detect_current_weapon(weapons_list):
    for index, weapon in enumerate(weapons_list):
        if weapon["image"] is not None:
            found_xy = None
            try:
                image_to_check = get_screen_area_as_image(weapon["check_area"])
                found_xy = search_image_in_image(weapon["image"], image_to_check)
            except:
                print("Can not read images. Resolution is wrong? Configs? Dunno :(")
            if found_xy:
                return index
    return None


class WeaponDetectorThread(threading.Thread):
    def __init__(self, weapon_list):
        threading.Thread.__init__(self)
        self.weapon_list = weapon_list
        self.out = None
        self.no_recoil = False
        self.shutdown = False

    def run(self):
        while not self.shutdown:
            if self.no_recoil:
                weapon_autodetect = detect_current_weapon(self.weapon_list)
                self.out = weapon_autodetect
            time.sleep(0.05)

    def terminate(self):
        self.shutdown = True


def main(weapon_filename):
    running = True
    no_recoil = False
    weapons_list, current_weapon_index = load_weapons(weapon_filename)
    overlay = OverlayLabel()
    overlay.set_size(20, 2)  # size in symbols
    print("INFO: Starting WeaponDetector daemon...")
    weapon_detector = WeaponDetectorThread(weapons_list)
    weapon_detector.setDaemon(True)
    weapon_detector.start()
    print("INFO: Everything looks ok, so I'm going to my general routine ;)")

    while running:
        if weapon_detector.out is not None:
            current_weapon_index = weapon_detector.out
        construct_overlay(overlay, weapons_list, current_weapon_index, no_recoil)
        if win32api.GetAsyncKeyState(F4):
            no_recoil = toggle_recoil(no_recoil)
            weapon_detector.no_recoil = no_recoil
            time.sleep(0.2)
        if win32api.GetAsyncKeyState(F10):
            running = not running
            beep_exit()
            weapon_detector.terminate()
            print("INFO: Exiting!")
            time.sleep(0.5)
        if win32api.GetAsyncKeyState(NUM_4):
            current_weapon_index = prev_weapon(weapons_list, current_weapon_index)
            time.sleep(0.2)
        if win32api.GetAsyncKeyState(NUM_6):
            current_weapon_index = next_weapon(weapons_list, current_weapon_index)
            time.sleep(0.2)
        if is_lmb_pressed() and no_recoil and not cursor_detector():
            process_no_recoil(overlay, weapons_list, current_weapon_index, no_recoil)
        time.sleep(0.01)


if __name__ == "__main__":
    if len(sys.argv) < 2 or (len(sys.argv) == 2 and sys.argv[1] == "help"):
        print("Usage: python " + sys.argv[0] + " <weapons_data_filename>")
        print("Example: python " + sys.argv[0] + " apex")
    else:
        data_filename = str(sys.argv[1])
        main(data_filename)
