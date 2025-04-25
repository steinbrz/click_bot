import pyautogui
import time
import random


def wiggle_dat_mouse():
    original_x, original_y = pyautogui.position()

    num_moves = random.randint(1,3)

    for i in range(num_moves):
        dx = random.randint(-10, 10)
        dy = random.randint(-10, 10)
        duration = random.uniform(0.1, 0.2)
        pyautogui.move(dx, dy, duration=duration)

    pyautogui.moveTo(original_x, original_y, duration=random.uniform(0.1, 0.2))

if __name__ == "__main__":
    # Number of clicks
    clicks = 800

    # Time delay between clicks (in seconds)
    delay = 1
    time.sleep(5)
    for i in range(clicks):

        
        pyautogui.click()  # Clicks at the current mouse position
        click_delay = random.uniform(.5, 1)
        time.sleep(click_delay)
        pyautogui.click()  # Clicks at the current mouse position
        time.sleep(click_delay)
        click_delay = random.uniform(3, 4)
        
        if random.randint(1, 10) == 1:
            wiggle_dat_mouse()

        # 1 in 20 chance for longer sleep
        if random.randint(1, 30) == 1:
            long_sleep = random.uniform(2, 6)
            time.sleep(long_sleep)
        # Take a break
        if i % 100 == 99:
            time.sleep(random.uniform(20, 30))
            wiggle_dat_mouse()


    