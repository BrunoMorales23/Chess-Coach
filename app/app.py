from flask import Flask, render_template, request, session
from playwright.sync_api import sync_playwright
import threading
from queue import Queue

app = Flask(__name__)
app.secret_key = '123'

browser = None
page = None
operation = False

browser_lock = threading.Lock()
page_lock = threading.Lock()
task_queue = Queue()

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
    initialize_browser()
    return render_template('initialize.html')

@app.route('/game', methods=['POST'])
def home():
        global operation
        print(operation)
        if operation == False:
            game_code = request.form.get('game-code')
            move_num = request.form.get('move-number')
            url = f"https://www.chess.com/game/live/{game_code}?move={move_num}"
            session['current_mov'] = move_num
            session['current_url'] = url
            url = session.get('current_url')
            p.goto(url)
            p.wait_for_selector("//div[contains(@class,'game-review-buttons-component')]", timeout=15000)
            p.screenshot(path="./static/images/ss.png", clip={"x": 195, "y": 70, "width": 555, "height": 550})
            operation = False
        else:
            url = session.get('current_url')
            search_browser(url=url)
            operation = False
        return render_template('index.html')

@app.route('/next', methods=['POST'])
def board_next():
    move_num = session.get('current_mov')
    move_num = int(move_num) + 1
    session['current_mov'] = move_num
    print(move_num)
    url = trim_url(move_num)
    url = url+str(move_num)
    print(url)
    session['current_url'] = url
    global operation
    operation = True
    return home()

@app.route('/previous', methods=['POST'])
def board_previous():
    move_num = session.get('current_mov')
    move_num = int(move_num) - 1
    session['current_mov'] = move_num
    url = trim_url(move_num)
    url = url+str(move_num)
    session['current_url'] = url

def initialize_browser():
    global browser
    global p
    playwright = sync_playwright().start()
    browser = playwright.chromium.launch(headless=False)
    p = browser.new_page()

def search_browser(url):
    global p
    p.goto(url)
    p.wait_for_selector("//div[contains(@class,'game-review-buttons-component')]", timeout=15000)
    p.screenshot(path="./static/images/ss.png", clip={"x": 195, "y": 70, "width": 555, "height": 550})

if __name__ == '__main__':
    app.run(debug=True, port=5000)


#browser.close()