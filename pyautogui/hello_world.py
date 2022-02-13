import pyautogui

location = pyautogui.locateCenterOnScreen("pyautogui/mercenaries.png", confidence=0.9)

pyautogui.click(location.x, location.y, clicks=1,interval=0.2, duration=0.2, button="left")
