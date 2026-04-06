# Use with corresponding systemd service file
import os
import signal
import subprocess

# make sure user is added to inputs group for evdev to work
import evdev

home = os.path.expanduser("~")

path_keys = "/dev/input/event5"
device_keys = evdev.InputDevice(path_keys)


def kbl_on(z1="110044", z2="222244", z3="222244", z4="110044", brightness="1"):
    subprocess.run(
        [
            f"{home}/PyVenv/l5p-kbl/bin/python3",  # venv python directly
            f"{home}/Stuff/Github/SystemPrograms/l5p-kbl/l5p_kbl.py",
            "static",
            z1,
            z2,
            z3,
            z4,
            "--brightness",
            brightness,
        ]
    )


def kbl_off(signum, frame):
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
            kbl_on()
            signal.alarm(60)
