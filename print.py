import time
import webbrowser
import pyautogui

webbrowser.open_new('C:\\OneDrive\\OneDrive - 잠신고등학교\\1_Coding\\life4cuts\\result.png')
time.sleep(3)
pyautogui.hotkey('ctrl', 'p')
time.sleep(3)
for i in range(3):
    pyautogui.hotkey('shift', 'tab')
pyautogui.press('enter')
time.sleep(1)
pyautogui.hotkey('alt', 'f4')
