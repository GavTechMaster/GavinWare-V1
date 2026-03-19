from pyjoystick.sdl2 import Key, Joystick, run_event_loop
import keyboard, os
os.environ["SDL_JOYSTICK_ALLOW_BACKGROUND_EVENTS"] = "1"
go = keyboard.press_and_release
cur = {
    'y': False,
    'r': False,
    'b': False,
    'w': False,
    'backspace': False,
    'enter': False,
    "5": False,
    "up": False,
    "down": False,
}
def get_cur():
    global cur
    return cur

def add_joy(*_):
    pass
def remove_joy(*_):
    pass
def key_received(key):
    global cur
    if key.keytype == Key.BUTTON:
        if key.value == 1:
            match int(key.__str__().split(' ')[1]):
                case 10: cur['y'] = True; go('a')
                case 9:  cur['r'] = True; go('w')
                case 11: cur['w'] = True; go('s')
                case 8:  cur['b'] = True; go('d')
    if key.keytype == Key.AXIS and key.value:
        if str(key).split(' ')[1] == "0": # If axis == x
            if key.value <= -.75:
                cur['backspace'] = True
                go('left')
            elif key.value >= .75:
                cur['enter'] = True
                go('right')
            else:
                cur['backspace'] = False
                cur['enter'] = False
        elif str(key).split(' ')[1] == "1": # If axis == y
            if key.value <= -.75: # -1 is UP!!
                cur['up'] = True
                go('up')
            elif key.value >= .75:
                cur['down'] = True
                go('down')
            else:
                cur['up'] = False
                cur['down'] = False
def start():
    run_event_loop(add_joy, remove_joy, key_received)

if __name__ == "__main__":
    start()