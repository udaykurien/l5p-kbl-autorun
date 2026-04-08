# Use with corresponding systemd service file
import os
import signal
import subprocess

# make sure user is added to inputs group for evdev to work
import evdev

light_on_k = False

home = os.path.expanduser("~")

# path_keys = "/dev/input/event5"
# device_keys = evdev.InputDevice(path_keys)


def find_keyboard():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        caps = device.capabilities()
        # Check if device generates key events
        if evdev.ecodes.EV_KEY in caps:
            keys = caps[evdev.ecodes.EV_KEY]
            # Look for common keyboard keys to be sure
            if evdev.ecodes.KEY_A in keys and evdev.ecodes.KEY_Z in keys:
                return device
    return None


device_keys = find_keyboard()

purple_splotch_low = {
    "z1": "110044",
    "z2": "222244",
    "z3": "222244",
    "z4": "110044",
    "b": "1",
}
purple_splotch_mid = {
    "z1": "220088",
    "z2": "444488",
    "z3": "444488",
    "z4": "220088",
    "b": "1",
}


def kbl_on(color=purple_splotch_low):
    global light_on_k
    light_on_k = True
    subprocess.run(
        [
            f"{home}/PyVenv/l5p-kbl/bin/python3",  # venv python directly
            f"{home}/Stuff/Github/SystemPrograms/l5p-kbl/l5p_kbl.py",
            "static",
            color["z1"],
            color["z2"],
            color["z3"],
            color["z4"],
            "--brightness",
            color["b"],
        ]
    )


def kbl_off(signum, frame):
    global light_on_k
    light_on_k = False
    subprocess.run(
        [
            f"{home}/PyVenv/l5p-kbl/bin/python3",  # venv python directly
            f"{home}/Stuff/Github/SystemPrograms/l5p-kbl/l5p_kbl.py",
            "off",
        ]
    )


signal.signal(signal.SIGALRM, kbl_off)

for event in device_keys.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        key_event = evdev.categorize(event)
        if key_event.keystate == evdev.KeyEvent.key_down:
            if not light_on_k:
                kbl_on(purple_splotch_mid)
            signal.alarm(60)
