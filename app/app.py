from flask import Flask, render_template, session, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)
app.secret_key = '123'
browser = None

#inicializar explorador + vista inicial
@app.route('/')
def index():
    global browser
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
    browser = webdriver.Chrome(options=chrome_options)
    return render_template('initialize.html')

#**********************************************************************************************************************
#lanzar la búsqueda del estado del tablero + inicializar vista de tablero
@app.route('/game', methods=['POST'])
def home():
    action = request.form.get("action")
    if action == "next":
        set_url(next=True)
        get_screenshot()
    elif action == "previous":
        set_url(next=False)
        get_screenshot()
    else:
        game_code = request.form.get('game-code')
        move_num = request.form.get('move-number')
        url = f"https://www.chess.com/game/live/{game_code}?move={move_num}"
        session['move-number'] = move_num
        session['game-code'] = game_code
        session['url'] = url
        get_screenshot()

    return render_template('index.html')

#**********************************************************************************************************************
#volver a la vista inicial
@app.route('/', methods=['POST'])
def reset():
    return render_template('initialize.html')

#**********************************************************************************************************************
#definir URL y establecer en las variables de sesión los valores de movimiento, código de partida y url
@app.route('/game')
def set_url(next):
    if next == True:
        move_num = session.get('move-number')
        move_num = int(move_num) + 1
        game_code = session.get('game-code')
        print(game_code)
        url = f"https://www.chess.com/game/live/{game_code}?move={move_num}"
        session['move-number'] = move_num
        session['url'] = url
    else:
        move_num = session.get('move-number')
        move_num = int(move_num) - 1
        game_code = session.get('game-code')
        url = f"https://www.chess.com/game/live/{game_code}?move={move_num}"
        session['move-number'] = move_num
        session['url'] = url 
    return

#**********************************************************************************************************************
#acceder al explorador en el movimiento y juego declarado para obtener la instancia actual del tablero
@app.route('/game')
def get_screenshot():
    global browser
    url = session.get('url')
    browser.get(url)
    anchor_dynamic_wait = WebDriverWait(browser, 10).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class,'game-review-buttons-component')]"))
    )

    board = browser.find_element("xpath", "//wc-chess-board[contains(@id,'board-single') and contains(@class,'board')]")
    board.screenshot('./static/images/ss.png')

if __name__ == '__main__':
    app.run(debug=True, port=5000)