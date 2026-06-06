print("Starting test script.\n\n")

from l5p_kbl_auto_v01 import find_keyboard, find_touchpad

device_key = find_keyboard()
device_touch = find_touchpad()

print(f"Keyboard device:\n{device_key}")
print("")
print(f"Touchpad device:\n{device_touch}")

print("\n\nFinished test script.")
