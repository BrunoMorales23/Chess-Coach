from flask import Flask, render_template, request, session
import asyncio
from playwright.sync_api import sync_playwright
import time
from waitress import serve

app = Flask(__name__)
app.secret_key = '123'

def trim_url(current_move):
    url = session.get('current_url')
    move_num = current_move
    digits = len(str(move_num))
    url = url[:-int(digits)]
    session['current_url'] = url
    print(url)
    return url

@app.route('/')
def index():
    return render_template('initialize.html')

@app.route('/game', methods=['POST'])
def home():
        if request.method == 'POST':
            game_code = request.form.get('game-code')
            move_num = request.form.get('move-number')
            url = f"https://www.chess.com/game/live/{game_code}?move={move_num}"
            session['current_mov'] = move_num
            session['current_url'] = url
            url = session.get('current_url')
            p = sync_playwright().start()
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)
            time.sleep(5)
            page.screenshot(path="./static/images/ss.png", clip={"x": 195, "y": 70, "width": 555, "height": 550})
            browser.close()
                    #return render_template('index.html')
        else:
                pass
            #return board()
        return render_template('index.html')

@app.route('/next', methods=['POST'])
def board():
 if request.method == 'POST':
        action = request.form.get('action')
        if action == 'Game Code' or action == 'Move Number':
            pass
        elif action == 'next':
            move_num = session.get('current_mov')
            move_num = int(move_num) + 1
            session['current_mov'] = move_num
            url = trim_url(move_num)
            url = url+str(move_num)
            session['current_url'] = url

        elif action == 'previous':
            move_num = session.get('current_mov')
            move_num = int(move_num) - 1
            session['current_mov'] = move_num
            url = trim_url(move_num)
            url = url+str(move_num)
            session['current_url'] = url


if __name__ == '__main__':
    app.run(debug=True, port=5000)