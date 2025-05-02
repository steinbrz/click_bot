from helper_functions import *
from 
import pyautogui
import time
import cv2
import random
from enum import Enum, auto
from rectangle import Rectangle

# BOTTOM = pyautogui.Point(x=742, y=551)
# MIDDLE = pyautogui.Point(x=697, y=513)
# TOP = pyautogui.Point(x=740, y=467)
INVENTORY_START = pyautogui.Point(x=1314, y=701)
INVENTORY_X_INC = 43
INVENTORY_Y_INC = 39
INVENTORY_ROWS = 7
INVENTORY_COLS = 4
SCALE_X, SCALE_Y = None, None


template_cache = {}

# START_BANK_CHEST = "/Users/zach/Dev/click_bot/images/blast_furnace/start_bank_chest.png"
TEST_IMAGE = "/Users/zach/Dev/click_bot/images/blast_furnace/test_image_coal_bank.png"

class BlastFurnacePositions(Enum):
    
    START_BANK_CHEST = "/Users/zach/Dev/click_bot/images/blast_furnace/start_bank_chest.png"
    COAL_IN_BANK = "/Users/zach/Dev/click_bot/images/blast_furnace/coal_bank.png"
    IRON_ORE_IN_BANK = "/Users/zach/Dev/click_bot/images/blast_furnace/iron_ore_bank.png"
    WITHDRAW_ALL = "/Users/zach/Dev/click_bot/images/blast_furnace/withdraw_all.png"
    DROP_ORE = pyautogui.Point(x=366, y=657)
    # ORE_COLLECT_BUTTON = pyautogui.Point(x=570, y=846)
    ORE_COLLECT_BUTTON = pyautogui.Point(x=261, y=888)
    OPEN_BANK_AFTER_ORE = pyautogui.Point(x=1004, y=390)
    COLLECT_BARS = pyautogui.Point(x=857, y=575)
    # COLLECT_BARS = pyautogui.Point(x=307, y=888)
    BANK_AFTER_COLLECT = pyautogui.Point(x=937, y=322)
    INVENOTRY_START = pyautogui.Point(x=1314, y=701)
    DEPOSIT_ALL = "/Users/zach/Dev/click_bot/images/blast_furnace/deposit_all.png"
    WITHDRAW_ALL_IRON = "/Users/zach/Dev/click_bot/images/blast_furnace/withdraw_all_iron_ore.png"



def find_position(position, debug=False) -> Rectangle:
    # Take screen shot
    if not debug:
        screenshot = capture_screenshot()
    else:
        screenshot = load_template_gray(TEST_IMAGE)
    # Load template
    if position not in template_cache:
        template_cache[position] = load_template_gray(position.value)
    # Look for template match
    rect = find_button_location(template_cache[position], screenshot)

    if debug:
        import pdb
        pdb.set_trace()
        debug_rectangle(rect, screenshot)
    
    return rect



def find_and_click_button(position: pyautogui.Point | str, right=False, delay=.2, debug=False) -> None:
    """
    Click the position provided
    """

    if isinstance(position.value, pyautogui.Point):
        move_mouse_random(position.value.x, position.value.y)
    elif isinstance(position.value, str):
        rect = find_position(position, debug=debug)
        print(f"Moving to x: {int(rect.center_x/SCALE_X)} y: {int(rect.center_x/SCALE_Y)}")
        move_mouse_scaled(rect.center_x, rect.center_y, SCALE_X, SCALE_Y)
    else:
        raise TypeError(f"Invalid type for position was passed as an argument. Got {type(position)} and expected str or pyautogui.Point")
    
    time.sleep(.5)
    
    if right:
        pyautogui.click(button="right")
    else:
        pyautogui.click()

    time.sleep(delay)


def open_bank_at_start(delay=.5, debug=False) -> None:
    """
    At start of run, find bank chest and open it
    """
    find_and_click_button(BlastFurnacePositions.START_BANK_CHEST, right=False, delay=delay, debug=debug)

def click_withdraw_all(delay=.5, debug=False) -> None:
    """
    When menu is open, click withdraw all
    """
    find_and_click_button(BlastFurnacePositions.WITHDRAW_ALL, right=False, delay=delay, debug=debug)

def withdraw_coal(delay=.5, debug=False) -> None:
    """
    With bank open, withdraw coal
    """
    find_and_click_button(BlastFurnacePositions.COAL_IN_BANK, right=True, delay=delay, debug=debug)
    click_withdraw_all()


def withdraw_iron_ore(delay=.5, debug=False) -> None:
    """
    With bank open, withdraw iron ore
    Args:
        delay (float): How long to wait after clicking
    Returns:
        None
    """
    find_and_click_button(BlastFurnacePositions.IRON_ORE_IN_BANK, right=True, delay=delay, debug=debug)
    find_and_click_button(BlastFurnacePositions.WITHDRAW_ALL_IRON, right=False, delay=delay)


def drop_ore(delay=10) -> None:
    """
    After withdrawing, drop ore at conveyor belt
    """
    find_and_click_button(BlastFurnacePositions.DROP_ORE, right=False, delay=delay)

def open_bank_after_drop_ore(delay=.5) -> None:
    """
    After dropping coal, go back an dopen bank
    """

    find_and_click_button(BlastFurnacePositions.OPEN_BANK_AFTER_ORE, right=False, delay=delay)

def collect_steel_bars(delay=1) -> None:
    """
    After placing coal and steel, collect steel bars
    """
    find_and_click_button(BlastFurnacePositions.COLLECT_BARS, delay=5)
    find_and_click_button(BlastFurnacePositions.ORE_COLLECT_BUTTON, delay=delay)


def open_bank_and_deposit(delay=1) -> None:
    """
    After collecting bars, open bank and deposit
    """
    find_and_click_button(BlastFurnacePositions.BANK_AFTER_COLLECT, delay=5)
    find_and_click_button(BlastFurnacePositions.INVENOTRY_START, right=True, delay=2)
    find_and_click_button(BlastFurnacePositions.DEPOSIT_ALL, delay=.5)


    











if __name__ == "__main__":
    
    time.sleep(5)
    SCALE_X, SCALE_Y = get_scale()
    while True:
        open_bank_at_start(delay=1)
        withdraw_coal(debug=False)
        drop_ore(delay=10)
        open_bank_after_drop_ore(delay=10)
        withdraw_iron_ore(delay=1)
        drop_ore(delay=10)
        time.sleep(8) # Wait for bars to cool
        collect_steel_bars()
        open_bank_and_deposit()






    



