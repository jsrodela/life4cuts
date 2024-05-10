import threading
import time
import webbrowser
import pyautogui
from main import settings


FILE_NAME = settings.PRINT_FILE_NAME


# only on windows
def activate_window(name):
    edge_windows = pyautogui.getWindowsWithTitle(name)[0]
    try:
        if edge_windows.isActive == False:
            edge_windows.activate()
        edge_windows.restore()
        if edge_windows.isMaximized == False:
            edge_windows.maximize()
    except Exception as e:
        edge_windows.minimize()
        edge_windows.maximize()
    return


def print_file(path: str, cnt: int):
    webbrowser.open_new(path)
    time.sleep(3)
    activate_window(FILE_NAME)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(5)
    for i in range(3):
        pyautogui.hotkey('tab')
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.press(str(cnt))
    for i in range(6):
        pyautogui.hotkey('shift', 'tab')
    pyautogui.press('enter')
    time.sleep(5)
    pyautogui.hotkey('alt', 'f4')


if __name__ == '__main__':
    print_file('C:\\OneDrive\\OneDrive - 잠신고등학교\\1_Coding\\life4cuts\\result.png', 3)
