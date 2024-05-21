import hear
from pynput import keyboard

key = keyboard.Key.space

current = set()

def on_press(key):
    current.add(key)
    hear.listen(True)

def on_release(key):
    current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()