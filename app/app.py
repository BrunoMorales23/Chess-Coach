from flask import Flask, render_template, request, session, redirect, url_for
from RPA.Browser.Selenium import Selenium
import pyautogui
from PIL import Image
import time

app = Flask(__name__)
app.secret_key = '123'
browser = Selenium()
width, height = pyautogui.size()
game_end = False
headless = True
tmp_ss_path = './tmp/ss.png'
output_path = './static/images/ss.png'

@app.route('/')
def initialize():
    return render_template('initialize.html')

@app.route('/game', methods=['POST'])
def home():
    if request.method == 'POST':
        game_code = request.form.get('game-code')
        session['game-code'] = game_code
        return redirect(url_for('work_phase'))
    return render_template('index.html')
       
@app.route('/game')
def work_phase():
    num_test = 0
    game_code = session.get('game-code')
    url = "https://www.chess.com/game/live/"+str(game_code)+'?move='+str(num_test)
    while game_end == False:
        if width == 1920 and height == 1080:
            if headless == True:
                    area = (190, 70, 875, 747)
            else:
                area = (210, 60, 1050, 885)

            try:
                browser.open_available_browser(url=url, headless=headless, maximized=True, browser_selection='chrome')
                #while game_end == False:
                browser.capture_page_screenshot(tmp_ss_path)
                img = Image.open(tmp_ss_path)
                final_ss = img.crop(area)
                final_ss.save(output_path)
            finally:
                browser.close_browser()
                time.sleep(1)
                num_test = num_test + 1
            return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

    #image = url_for('static', filename='ss.png')
    #return render_template('index.html', pic=image)