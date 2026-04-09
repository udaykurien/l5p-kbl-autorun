# Use with corresponding systemd service file
import os
import subprocess
import threading

# make sure user is added to inputs group for evdev to work
import evdev

light_on_k = False

timer = None

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

home = os.path.expanduser("~")


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


def find_touchpad():
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        caps = device.capabilities()
        # Check if device generates absolute axis events
        if evdev.ecodes.EV_ABS in caps:
            # Check which specific absolute capabilites are present
            abs_caps = caps[evdev.ecodes.EV_ABS]
            # Extract absolute axis
            axes = [abs_cap[0] for abs_cap in abs_caps]
            # Check if device contains multitouch slot, MT X, MT ID etc
            if (
                (evdev.ecodes.ABS_MT_SLOT in axes)
                and (evdev.ecodes.ABS_MT_POSITION_X in axes)
                and (evdev.ecodes.ABS_MT_TRACKING_ID in axes)
            ):
                return device
    return None


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


def kbl_off():
    global light_on_k
    light_on_k = False
    subprocess.run(
        [
            f"{home}/PyVenv/l5p-kbl/bin/python3",  # venv python directly
            f"{home}/Stuff/Github/SystemPrograms/l5p-kbl/l5p_kbl.py",
            "off",
        ]
    )


def timer_reset():
    global timer
    if timer is not None:
        timer.cancel()
    timer = threading.Timer(60, kbl_off)
    timer.start()


if __name__ == "__main__":
    device_keys = find_keyboard()
    for event in device_keys.read_loop():
        if event.type == evdev.ecodes.EV_KEY:
            key_event = evdev.categorize(event)
            if key_event.keystate == evdev.KeyEvent.key_down:  # type: ignore
                if not light_on_k:
                    kbl_on(purple_splotch_mid)
                timer_reset()
