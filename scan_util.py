import json
import Levenshtein
import pytesseract
import win32gui
from PIL import Image, ImageGrab

NAME_X = 270 / 1920
NAME_X_END = 1525 / 1920
COMPLETED_X = 1680 / 1920
COMPLETED_X_END = 1835 / 1920
NAME_Y = [255 / 1080, 410 / 1080, 570 / 1080, 725 / 1080, 885 / 1080, 880 / 1080]
COMPLETED_Y = [(x * 1080 + 20) / 1080 for x in NAME_Y]
FONT_HEIGHT = 40 / 1080  # ? idk

default_whitelist = """abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ()-, 0123456789'"!?/ö"""

hwnd = win32gui.FindWindow("UnityWndClass", "Honkai: Star Rail")
window_width, window_height = win32gui.GetClientRect(hwnd)[2:]
window_x, window_y = win32gui.ClientToScreen(hwnd, (0, 0))
x_scaling_factor = window_width / 1920
y_scaling_factor = window_height / 1080

pytesseract.pytesseract.tesseract_cmd = "tesseract/tesseract.exe"

data = {}


def load_data():
    global data
    if not data:
        with open('processed_data.json', 'r', encoding='utf-8') as proc_data_file:
            data = json.load(proc_data_file)


# shamelessly stolen from https://github.com/kel-z/HSR-Scanner/blob/main/src/utils/screenshot.py#L152
def take_screenshot(x: float, y: float, width: float, height: float):
    x = window_x + int(window_width * x)
    y = window_y + int(window_height * y)
    width = int(window_width * width)
    height = int(window_height * height)
    screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height), all_screens=True)
    screenshot = screenshot.resize((int(width / x_scaling_factor), int(height / y_scaling_factor)))
    return screenshot


def image_to_string(img: Image, psm=7, whitelist=None) -> str:
    if whitelist:
        config = f'-c tessedit_char_whitelist="{whitelist}" --psm {psm} -l DIN-Alternate'
    else:
        config = f'--psm {psm} -l DIN-Alternate'
    return pytesseract.image_to_string(img, config=config).replace("\n", " ").strip()


def get_achievement_name(index: int) -> str:  # index stars at 0
    index = min(index, 4)
    img = take_screenshot(NAME_X, NAME_Y[index], NAME_X_END - NAME_X, FONT_HEIGHT)
    return image_to_string(img)


def get_completed_status(index: int) -> bool:
    index = min(index, 4)
    img = take_screenshot(COMPLETED_X, COMPLETED_Y[index], COMPLETED_X_END - COMPLETED_X, FONT_HEIGHT)
    return Levenshtein.ratio(image_to_string(img, whitelist='Completed'), 'Completed') >= 0.5


def get_closest_name_match(index: int):
    name_from_image = get_achievement_name(index)
    maxCost = 0.
    maxName = ""
    for chiveName in data.keys():
        cost = Levenshtein.ratio(name_from_image, chiveName)
        if cost > maxCost:
            maxCost = cost
            maxName = chiveName
    if maxCost < 0.5:
        raise ValueError("No close match")
    return maxName, data[maxName]
