# Use with corresponding systemd service file
import os
import select
import subprocess
import threading
import json

# make sure user is added to input group for evdev to work
import evdev

light_on_k = False
light_on_t = False

bl_time_1 = 30  # Backlight time when key is pressed (s)/run/current-system/sw/bin/python3
bl_time_2 = 45  # Backlight time when key is pressed (s)/run/current-system/sw/bin/python3
bl_time_3 = 4   # Backlight time when touchpad is used (s)
bl_time_4 = 10  # Backlight time when touchpad is used, while backlight from key is still active (s)

timer = None

home = os.path.expanduser("~")

with open(f"{home}/Stuff/Github/SystemPrograms/l5p-kbl-autorun/NixOS/colors.json", "r") as f:
    colors = json.load(f)

default_color =  colors["salmon"]
selected_color_1 =  colors["cyber_purple_red"]
selected_color_2 =  colors["purple_high"]

# NixOS: use system python instead of venv python so pyusb can find libusb
# via LD_LIBRARY_PATH set in the systemd service environment
PYTHON = "/run/current-system/sw/bin/python3"
L5P_KBL = f"{home}/Stuff/Github/SystemPrograms/l5p-kbl/l5p_kbl.py"


def find_keyboard():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        caps = device.capabilities()
        if evdev.ecodes.EV_KEY in caps:
            keys = caps[evdev.ecodes.EV_KEY]
            if evdev.ecodes.KEY_A in keys and evdev.ecodes.KEY_Z in keys:
                return device
    return None


def find_touchpad():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        caps = device.capabilities()
        if evdev.ecodes.EV_ABS in caps:
            abs_caps = caps[evdev.ecodes.EV_ABS]
            axes = [abs_cap[0] for abs_cap in abs_caps]
            if (
                (evdev.ecodes.ABS_MT_SLOT in axes)
                and (evdev.ecodes.ABS_MT_POSITION_X in axes)
                and (evdev.ecodes.ABS_MT_TRACKING_ID in axes)
            ):
                return device
    return None


# NixOS: subprocess calls now use PYTHON/L5P_KBL instead of venv paths
def kbl_on(color=default_color):
    global light_on_k
    light_on_k = True
    subprocess.run([PYTHON, L5P_KBL, "static", color["z1"], color["z2"], color["z3"], color["z4"], "--brightness", color["b"]])


def kbl_breath(color=default_color):
    global light_on_t
    light_on_t = True
    subprocess.run([PYTHON, L5P_KBL, "breath", color["z1"], color["z2"], color["z3"], color["z4"], "--brightness", color["b"]])


def kbl_hue():
    global light_on_t
    light_on_t = True
    subprocess.run([PYTHON, L5P_KBL, "hue"])


def kbl_off():
    global light_on_k, light_on_t
    light_on_k = False
    light_on_t = False
    subprocess.run([PYTHON, L5P_KBL, "off"])


def timer_reset(sec):
    global timer
    if timer is not None:
        timer.cancel()
    timer = threading.Timer(sec, kbl_off)
    timer.start()


if __name__ == "__main__":
    while True:
        try:
            # NixOS: moved device detection inside loop so devices are
            # re-detected on error (e.g. after keyboard shortcut turns
            # backlight off and disrupts the device handle)
            device_keys = find_keyboard()
            device_touch = find_touchpad()

            print(f"Keyboard: {device_keys}")
            print(f"Touchpad: {device_touch}")

            devices_to_monitor = [d for d in [device_keys, device_touch] if d is not None]

            readable, _, _ = select.select(devices_to_monitor, [], [])
            for device in readable:
                if device == device_keys:
                    for event in device_keys.read():
                        if event.type == evdev.ecodes.EV_KEY:
                            key_event = evdev.categorize(event)
                            if key_event.keystate == evdev.KeyEvent.key_down:
                                if not light_on_k:
                                    kbl_on(selected_color_1)
                                timer_reset(bl_time_2)
                if device == device_touch:
                    for event in device_touch.read():
                        if not light_on_k and not light_on_t:
                            kbl_on(selected_color_1)
                        timer_reset(bl_time_2)

        except Exception as e:
            # NixOS: catch all errors and continue instead of exiting,
            # so the service recovers automatically without a restart
            print(f"Error: {e}, restarting...")
            continue
