import vgamepad as vg
import time

debug = False

gamepad = None
def load_gamepad():
    global gamepad
    gamepad = vg.VX360Gamepad()


def wake_up():
    if gamepad is None:
        raise ValueError('GamepadNotInitialized')
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    gamepad.update()
    time.sleep(0.5)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_UP)
    gamepad.update()
    time.sleep(0.5)
    if debug:
        print("pressed dpad_up to wake up")


def go_down():
    if gamepad is None:
        raise ValueError('GamepadNotInitialized')
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    gamepad.update()
    time.sleep(0.05)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_DPAD_DOWN)
    gamepad.update()
    time.sleep(0.2) # to wait to go down
    if debug:
        print("pressed dpad_down")


def change_tab():
    if gamepad is None:
        raise ValueError('GamepadNotInitialized')
    gamepad.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.update()
    time.sleep(0.05)
    gamepad.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
    gamepad.update()
    time.sleep(0.2) # to wait for the tab to load
    if debug:
        print("pressed right_thumb")
