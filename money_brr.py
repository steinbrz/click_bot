import pyautogui
import time
import random

# Number of clicks
clicks = 103

# Time delay between clicks (in seconds)
delay = 1
time.sleep(5)
for i in range(clicks):

    
    pyautogui.click()  # Clicks at the current mouse position
    # time.sleep(click_delay)
    click_delay = random.uniform(.5, 1)
    pyautogui.click()  # Clicks at the current mouse position
    time.sleep(click_delay)
    click_delay = random.uniform(3, 4)
    time.sleep(click_delay)
    
        # 1 in 20 chance for longer sleep
    if random.randint(1, 20) == 1:
        long_sleep = random.uniform(5, 10)
        time.sleep(long_sleep)


    