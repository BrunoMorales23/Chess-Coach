from flask import Flask, render_template, session, request, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os

app = Flask(__name__)
app.secret_key = '123'
browser = None
next_button = None
prev_button = None
output_path = './static/images/ss.webp'
streaming_game = False
filename_value = ''
root = "C:/Users/MarsuDIOS666/Desktop/Chess Coach App/app/static/images/ss.webp"
target_root = "C:/Users/MarsuDIOS666/Desktop/Chess Coach App/app/static/images/"

#inicializar explorador + vista inicial
@app.route('/')
def index():
    global browser
    chrome_options = Options()
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    browser = webdriver.Chrome(options=chrome_options) #service=service)
    login(user="chesscoachselenium@gmail.com" , password="ChessCoach2303@")
    return render_template('initialize.html')

#lanzar la búsqueda del estado del tablero + inicializar vista de tablero
@app.route('/game', methods=['POST'])
def home():
    global browser
    global streaming_game
    action = request.form.get("action")
    match (action, streaming_game):
        case ("next", True):
            next_move(next=True)
            time.sleep(0.1)
            get_screenshot()
            render_value = "dynamicIndex.html"
        case ("next" , False):
            next_move(next=True)
            time.sleep(0.1)
            get_screenshot()
            render_value = "index.html"
        case ("previous", True):
            next_move(next=False)
            time.sleep(0.1)
            get_screenshot()
            render_value = "dynamicIndex.html"
        case ("previous" , False):
            next_move(next=False)
            time.sleep(0.1)
            get_screenshot()
            render_value = "index.html"
        case _:
            game_code = request.form.get('game-code')
            move_num = request.form.get('move-number')
            url = f"https://www.chess.com/game/live/{game_code}?move={move_num}"
            session['move-number'] = move_num
            session['game-code'] = game_code
            session['url'] = url
            url = session.get('url')
            browser.get(url)
            live_game = get_screenshot()
            if live_game == True:
                streaming_game = True
                render_value = "dynamicIndex.html"
            else:
                streaming_game = False
                render_value = "index.html"
    return render_template(render_value)

#establecer imagen dinámica
@app.route('/dynamic-index', methods=['GET', 'POST', 'DELETE'])
def get_image():
    if request.method == 'POST':
        global filename_value
        get_screenshot()
        data = request.get_json()
        filename = data.get("filename")
        os.rename(root, target_root+filename)
        filename_value = "/static/images/"+filename
        time.sleep(10)
        return send_file(filename_value, mimetype='image/webp')
    elif request.method == 'DELETE':
        data = request.get_json()
        filename = data.get('filename')
        filename = target_root+filename
        os.remove(filename)
        return jsonify({"message": "Archivo eliminado correctamente."}), 200
    elif request.method == 'GET':
        return jsonify({"filename": filename_value}), 200


#volver a la vista inicial
@app.route('/', methods=['POST'])
def reset():
    return render_template('initialize.html')


#definir URL y establecer en las variables de sesión los valores de movimiento, código de partida y url
@app.route('/game')
def next_move(next):
    global next_button
    global prev_button
    if next == True:
        if next_button ==  None:
            xpath_code = "//button[contains(@aria-label,'Forward')]"
            next_button = browser.find_element(By.XPATH, xpath_code)
        next_button.click()
    else:
        if prev_button ==  None:
            xpath_code = "//button[contains(@aria-label,'Back')]"
            prev_button = browser.find_element(By.XPATH, xpath_code)
        prev_button.click()
    return

#acceder al explorador en el movimiento y juego declarado para obtener la instancia actual del tablero
@app.route('/game')
def get_screenshot():
    try:
        xpath_code = "//div[contains(@class,'game-review-buttons-component')]"
        WebDriverWait(browser, 5).until(
        EC.visibility_of_element_located((By.XPATH, xpath_code))
        )
        xpath_code = "//wc-chess-board[contains(@id,'board-single') and contains(@class,'board')]"
        board = browser.find_element("xpath", xpath_code)
        board.screenshot('./static/images/ss.webp')
        live_game = False
    except TimeoutException:
        xpath_code = "//wc-chess-board[contains(@id,'board-single') and contains(@class,'board')]"
        board = browser.find_element("xpath", "//wc-chess-board[contains(@id,'board-single') and contains(@class,'board')]")
        board.screenshot(output_path)
        live_game = True
        return live_game

def login(user, password):
    browser.get('https://www.chess.com/login')
    xpath_code =  "//input[contains(@placeholder,'Username')]"
    input_user = browser.find_element(By.XPATH, xpath_code)
    input_user.send_keys(user)
    xpath_code = "//input[contains(@placeholder,'Password')]"
    input_pass = browser.find_element(By.XPATH, xpath_code)
    input_pass.send_keys(password)
    xpath_code = "//button[contains(text(),'Log In')]"
    login_button = browser.find_element(By.XPATH, xpath_code)
    login_button.click()
    try:
        xpath_code = "//a[contains(text(),'ChessCoachSelenium')]"
        WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath_code))
        )
        print("LogIn Successful")
        pass
    except TimeoutException:
        raise Exception("Unable to LogIn, failed at def 'login'")
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)