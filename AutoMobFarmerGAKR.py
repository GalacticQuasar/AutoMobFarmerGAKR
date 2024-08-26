import keyboard
import mouse
import time
import threading


def start_stop(key_event: keyboard.KeyboardEvent):
    print("Program", "ACTIVATING" if not toggle_event.is_set() else "DEACTIVATING")

    if toggle_event.is_set():
        toggle_event.clear()
        if option == 2:
            timer.cancel()
    else:
        toggle_event.set()
        if option == 2:
            restart_timer()


def clicker():
    print("INITIALIZING CLICKER THREAD")
    while True:
        toggle_event.wait()
        print("CLICKING")
        mouse.click("left")
        time.sleep(click_interval)


def clicker_and_eater():
    print("INITIALIZING CLICKER THREAD")
    while True:
        toggle_event.wait()
        eating.wait()
        print("CLICKING")
        mouse.click("left")
        time.sleep(click_interval)


def eating_fun():
    print("INITIALIZING EATING THREAD")
    toggle_event.wait()
    print("EATING")
    eating.clear()
    time.sleep(1)  # buffer to ensure click does not interfere with right click
    mouse.press(mouse.RIGHT)
    time.sleep(1.65)
    mouse.release(mouse.RIGHT)
    eating.set()
    restart_timer()


def restart_timer():
    print("RESTARTING TIMER")
    global timer
    timer.cancel()
    timer = threading.Timer(eat_interval, eating_fun)
    timer.start()


option = int(input("Choose:\n"
                   "1: Basic Clicker\n"
                   "2: Clicker with Eating (KEEP FOOD IN OFF-HAND)\n"))

toggle_event = threading.Event()
toggle_event.clear()

if option == 2:
    click_function = clicker_and_eater
    eating = threading.Event()
    eating.set()
    print("<Clicker With Eater> SELECTED")
else:
    click_function = clicker
    print("<BASIC CLICKER> SELECTED")

click_interval = float(input("Enter the click interval (in seconds) that you wish to operate with: "))
if option == 2:
    eat_interval = float(input("Enter the eating interval (in minutes) that you wish to eat at: ")) * 60
    timer = threading.Timer(eat_interval, eating_fun)

print("The start and stop key is ALT. To EXIT the program, press backtick/tilde key '`'")
print("Press ALT when you are ready to start farming! I will click at", round(1 / click_interval, ndigits=1),
      "clicks per second!")

keyboard.on_release_key("alt", start_stop)

clicking_thread = threading.Thread(target=click_function, daemon=True)
clicking_thread.start()

keyboard.wait('`')
