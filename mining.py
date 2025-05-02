from helper_functions import (
    capture_screenshot,
    load_pattern, 
    find_objects, 
    move_mouse_scaled, 
    find_button,
    get_scale,
    move_mouse_random
)
import pyautogui
import time
import cv2
import random

BOTTOM = pyautogui.Point(x=742, y=551)
MIDDLE = pyautogui.Point(x=697, y=513)
TOP = pyautogui.Point(x=740, y=467)
INVENTORY_START = pyautogui.Point(x=1314, y=701)
INVENTORY_X_INC = 43
INVENTORY_Y_INC = 39
INVENTORY_ROWS = 7
INVENTORY_COLS = 4

IRON_ORE_SINGLE_IMG = "/Users/zach/Dev/click_bot/images/iron_ore_single_3.png"
DROP_ORE_BUTTON = "/Users/zach/Dev/click_bot/images/drop_ore_button.png"

def mine_cycle():

    MINING_SPOTS = [BOTTOM, MIDDLE, TOP]
    random.shuffle(MINING_SPOTS)
    for spot in MINING_SPOTS:
        move_mouse_random(spot.x, spot.y, duration=.1, range=.15)
        time.sleep(random.uniform(2.5, 3.5))
        pyautogui.click()
        if random.randint(0, 20) == 1:
            time.sleep(random.uniform(1, 5))


    # pyautogui.moveTo(x=BOTTOM.x, y=BOTTOM.y, duration=.05)
    # pyautogui.click()
    # time.sleep(3)

    # pyautogui.moveTo(x=MIDDLE.x, y=MIDDLE.y, duration=.05)
    # pyautogui.click()
    # time.sleep(3)

    # pyautogui.moveTo(x=TOP.x, y=TOP.y, duration=.05)
    # pyautogui.click()
    # time.sleep(3)

def get_ore_in_inventory():

    img = capture_screenshot()
    template = load_pattern(IRON_ORE_SINGLE_IMG)
    ore_locations = find_objects(template, img)
    return ore_locations

def click_drop_ore_button(scale_x, scale_y):

    img = capture_screenshot()
    template = load_pattern(DROP_ORE_BUTTON)
    drop_button_loc, button_h, button_w = find_button(template, img)
    button_center_x = drop_button_loc[0] + button_w / 2
    button_center_y = drop_button_loc[1] + button_h / 2
    move_mouse_scaled(button_center_x, button_center_y, scale_x, scale_y)
    pyautogui.click()

def drop_ore(ore_locations, scale_x, scale_y):

    for item in ore_locations:
        item_center_x = item[0] + (item[2] / 2)
        item_center_y = item[1] + (item[3] / 2)
        move_mouse_scaled(item_center_x, item_center_y, scale_x, scale_y)
        time.sleep(.2)
        # Right click using pyautogui
        pyautogui.rightClick()
        time.sleep(.2)

        click_drop_ore_button(scale_x, scale_y)
        time.sleep(.5)






if __name__ == "__main__":
    
    time.sleep(5)
    scale_x, scale_y = get_scale()
    
    while True:
        mine_cycle()
        if random.randint(0, 5) == 1:
            time.sleep(random.uniform(4, 8))

        ore_locations = get_ore_in_inventory()
        if len(ore_locations) >= 20:
            drop_ore(ore_locations, scale_x, scale_y)

    # drop_ore()

    # img = capture_screenshot()
    # template = load_pattern(IRON_ORE_SINGLE_IMG)
    # ore = find_objects(template, img)
    # drop_ore(ore, img)

    # ys, xs = np.where(res >= threshold)
    # rects = []
    # for (x, y) in zip(xs, ys):
    #     rects.append([int(x), int(y), tw, th])

    # # 5. (Optional but recommended) Group overlapping detections
    # #    This merges nearby/overlapping boxes into single detections.
    # rects, weights = cv2.groupRectangles(rects, groupThreshold=1, eps=0.5)

    # # 6. Count them
    # count = len(rects)
    # print(f"Found {count} occurrences.")

    # # 7. (Optional) Draw boxes to verify
    # for (x, y, w, h) in rects:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow('Matches', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



