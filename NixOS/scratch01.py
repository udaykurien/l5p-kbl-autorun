import os
import signal
import subprocess

# make sure user is added to inputs group for evdev to work
import evdev

home = os.path.expanduser("~")

print(evdev.ecodes.EV_ABS)
print(evdev.ecodes.ABS_MT_SLOT)
print(evdev.ecodes.ABS_MT_POSITION_X)
print(evdev.ecodes.ABS_MT_POSITION_Y)
print(evdev.ecodes.ABS_MT_TOUCH_MAJOR)
print(evdev.ecodes.ABS_MT_TRACKING_ID)


print("\n")

# for path in evdev.list_devices():
#     print(evdev.InputDevice(path))


def find_touchpad():
    print("-" * 50)
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        caps = device.capabilities()
        if evdev.ecodes.EV_ABS in caps:
            print("Device with abs caps:")
            print(device)
            print(device.capabilities())
            print("")
            print("keys:")
            keys = caps[evdev.ecodes.EV_ABS]
            print(keys)
            axis = [key[0] for key in keys]
            print("\nkeys first entry:")
            print(axis)
            print("-" * 50)
            if (
                (evdev.ecodes.ABS_MT_SLOT in axis)
                and (evdev.ecodes.ABS_MT_POSITION_X in axis)
                and (evdev.ecodes.ABS_MT_TRACKING_ID in axis)
            ):
                print(device)
                return device


device_touch = find_touchpad()

print("")

# device_touch = evdev.InputDevice("/dev/input/event9")
print(device_touch)

print("\n")

caps = device_touch.capabilities()
print(caps)

for event in device_touch.read_loop():
    print(evdev.categorize(event))
