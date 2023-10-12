from PIL import Image,ImageGrab
import win32gui,win32process
from ctypes import windll #scaling
import pytesseract 
import os
from deep_translator import GoogleTranslator
#Reason for using pytesseract is that, it seems to be the fastest, 
#I tried using easyocr but took up too much memory, 500MB-700MB~

#For Scaling Purposes
user32 = windll.user32
user32.SetProcessDPIAware()

#Set location for ocr
tesseract_folder = os.path.abspath("extra/Tesseract-OCR/tesseract.exe")
try:
    pytesseract.pytesseract.tesseract_cmd = tesseract_folder
except(FileNotFoundError):
    print('File Could Not Be Found')
    pass

#Returns a list of active windows
def returnWindowList(hwnd, lists):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)
        if title and right-left and bottom-top:
            lists.append(title)

#Check if window exists
def _get_active_window(window):
    hwnd = win32gui.FindWindow(None, window)
    if not (hwnd ==0):
        return True
    else:
        return False
#Takes a screenshot of the chosen window and takes a screnshot
def screenshot_current_window(window):
    hwnd = win32gui.FindWindow(None, window)
    hwndDC = win32gui.GetWindowDC(hwnd)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w_height = (bottom-top)
    w_width = (right-left)  
    screenshot = ImageGrab.grab(bbox=(win32gui.GetWindowRect(hwnd)))
    screenshot.save('temp\\temp.jpg')
    
def translate_text():
    
    jp_string_text = pytesseract.image_to_string(Image.open('temp\\temp.jpg'), lang='jpn')
    en_string_text = GoogleTranslator(source='japanese', target='en').translate(jp_string_text)
    return jp_string_text, en_string_text


def get_active_windows():
    active_window_list = [] 
    win32gui.EnumWindows(returnWindowList, active_window_list)
    for window in active_window_list: 
        hwnd = win32gui.FindWindow(None, window)
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        active_window_list[active_window_list.index(window)] = ("pid({})".format(str(pid)) +window  )
    active_window_list = list(dict.fromkeys(active_window_list))
    return active_window_list


