from RPA.Browser.Selenium import Selenium
from PIL import Image
import pyautogui
import time

browser = Selenium()
width, height = pyautogui.size()
game_end = False
tmp_ss_path = './tmp/ss.png'
output_path = './app/static/images/ss.png'

if width == 1920 and height == 1080:
    live_code = input(f'Please, declare live game code:  ')
    url = "https://www.chess.com/game/live/"+live_code+'?move=0'
    #popup_end_game_template = Image.open('./templates/cross.png')
    area = (210, 60, 1050, 885)
    

    try:
        browser.open_available_browser(url=url, headless=False, maximized=True, browser_selection='chrome')
        while game_end == False:
            browser.capture_page_screenshot(tmp_ss_path)
            img = Image.open(tmp_ss_path)
            final_ss = img.crop(area)
            final_ss.save(output_path)
            input("ASD")

    finally:
        browser.close_browser()


else:
    pass