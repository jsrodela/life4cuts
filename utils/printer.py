import threading
import time
import webbrowser
import pyautogui


def print_file(path: str, cnt: int):
    webbrowser.open_new(path)
    time.sleep(3)
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(5)
    for i in range(3):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press(str(cnt))
    for i in range(6):
        pyautogui.hotkey('shift', 'tab')
    pyautogui.press('enter')
    time.sleep(3)
    pyautogui.hotkey('alt', 'f4')


if __name__ == '__main__':
    print_file('C:\\OneDrive\\OneDrive - 잠신고등학교\\1_Coding\\life4cuts\\result.png', 3)
