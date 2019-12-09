from evdev import uinput, ecodes as e
import time

with uinput.UInput() as ui:
    while (1):
        ui.write(e.EV_KEY, e.KEY_J, 1)
        ui.write(e.EV_KEY, e.KEY_J, 0)
        ui.syn()
        time.sleep(5)
