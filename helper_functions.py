import mss
import cv2
import numpy as np
import pyautogui
import random
from rectangle import Rectangle

NEW_USER_IMG_PATH = "/Users/zach/Dev/click_bot/images/new_user_image.png"
VS_CODE_TEST_IMG_PATH = "/Users/zach/Dev/click_bot/images/vscode_example.png"

TWEENS = [
    pyautogui.linear,
    pyautogui.easeInOutBounce,
    pyautogui.easeInOutBack,
    pyautogui.easeInOutElastic,
    pyautogui.easeInOutCirc,
    pyautogui.easeOutExpo
]


def get_scale():

    with mss.mss() as sct:
        shot = sct.grab(sct.monitors[1])

    # 2. run template matching (…as before…) to get rects = [(x,y,w,h),…]
    #    assume rects is populated

    # 3. get physical vs. logical screen size
    phys_w, phys_h = shot.width, shot.height
    log_w, log_h   = pyautogui.size()

    scale_x = phys_w / log_w
    scale_y = phys_h / log_h
    return scale_x, scale_y

def get_center_of_button(x, y, width, height):

    return x + (width/2), y + (height/2)

def move_mouse_random(x, y, duration=.1, range=.1):
    tween = random.choice(TWEENS)
    duration = random.uniform(duration-(range/2), duration+(range/2))
    pyautogui.moveTo(x=x, y=y, duration=duration, tween=tween)

def move_mouse_scaled(x, y, scale_x, scale_y, duration=.05):

    # random tween
    tween = random.choice(TWEENS)  
    pyautogui.moveTo(x=int(x/scale_x), y=int(y/scale_y), duration=duration, tween=tween)

def capture_screenshot():

    with mss.mss() as sct:
        # grab the entire primary monitor
        monitor = sct.monitors[1]
        sct_img = sct.grab(monitor)

        # mss returns BGRA; convert to BGR for OpenCV
        img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_BGRA2BGR)

        # Grey Conversion(Should be faster for comparing)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
    return img


def load_pattern(img_path):
    
    # template = cv2.imread("my_template.png", cv2.IMREAD_COLOR)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv2.imshow('Screenshot', img)     # pop up a window
    # cv2.waitKey(0)                        # wait for any key
    # cv2.destroyAllWindows() 

    return img

def load_template_gray(img_path):
    """Load template image with gray color scale"""
    
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return img


def find_button(template, img):
    scale_x, scale_y = get_scale()

    th, tw = template.shape[:2]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    threshold = .8

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    return max_loc, th, tw

def find_button_location(template, img) -> Rectangle:
    """ Find strong match of template to screenshot and return center of object to press"""

    th, tw = template.shape[:2]
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    return Rectangle(x=max_loc[0], y=max_loc[1], width=tw, height=th)



def find_objects(template, img):

    th, tw = template.shape[:2]
    # perform normalized cross-correlation
    # pdb.set_trace()
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    # get the best match position
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # pyautogui.moveTo(max_loc.x, max_loc.y, duration=.1)


    print(max_loc)
    threshold = .7
    ys, xs = np.where(res >= threshold)
    rects = []
    for (x, y) in zip(xs, ys):
        rects.append([int(x), int(y), tw, th])

    # 5. (Optional but recommended) Group overlapping detections
    #    This merges nearby/overlapping boxes into single detections.
    rects, weights = cv2.groupRectangles(rects, groupThreshold=1, eps=0.5)

    # 6. Count them
    # random.shuffle(rects)
    np.random.shuffle(rects)
    count = len(rects)
    print(f"Found {count} occurrences.")

    # 7. (Optional) Draw boxes to verify
    # for (x, y, w, h) in rects:
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow('Matches', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # pdb.set_trace()

    return rects


def debug_rectangle(rect, img):

    cv2.rectangle(img, (rect.x, rect.y), (rect.x + rect.width, rect.y + rect.height), (0, 255, 0), 2)
    cv2.imshow('Matches', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()





# Debug
if __name__ == "__main__":
    img = capture_screenshot()
    pattern = load_pattern(VS_CODE_TEST_IMG_PATH)
    # find_coordinate(pattern, img)