from flask import Flask, render_template, session, request, send_file, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import json


app = Flask(__name__)
config_path = 'C:/Users/MarsuDIOS666/Desktop/CHESS-COACH-MAIN/config.json'
config_data = {}
app.secret_key = '123'
browser = None
next_button = None
prev_button = None
output_path = './static/images/ss.webp'
streaming_game = False
filename_value = ''
#root = "C:/Users/MarsuDIOS666/Desktop/Chess Coach App/app/static/images/ss.webp"
#target_root = "C:/Users/MarsuDIOS666/Desktop/Chess Coach App/app/static/images/"
root = ""
target_root = ""

#inicializar explorador + vista inicial
@app.route('/', methods=['POST', 'GET'])
def index():
    global browser
    if request.method == 'POST':
        #volver a la vista inicial
        return render_template('initialize.html')
    else:
        get_config_file(config_path)
        set_initial_paths(priv_env=True)
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--ignore-certificate-errors")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        browser = webdriver.Chrome(options=chrome_options) #service=service)
        login(user="XXX@gmail.com" , password="XXX")
    return render_template('initialize.html')

#lanzar la búsqueda del estado del tablero + inicializar vista de tablero
@app.route('/game', methods=['POST'])
def home():
    global browser
    global streaming_game
    action = request.form.get("action")
    match (action, streaming_game):
        #case ("next", True):
        #    next_move(next=True)
        #    time.sleep(0.1)
        #    get_screenshot()
        #    render_value = "dynamicIndex.html"
        case ("next" , False):
            next_move(next=True)
            time.sleep(0.1)
            get_screenshot()
            render_value = "index.html"
        #case ("previous", True):
        #    next_move(next=False)
        #    time.sleep(0.1)
        #    get_screenshot()
        #    render_value = "dynamicIndex.html"
        case ("previous" , False):
            next_move(next=False)
            time.sleep(0.1)
            get_screenshot()
            render_value = "index.html"
        case ("switch", False):
            config_xpath_code = "//button[contains(@id,'board-controls-settings')]"
            switch_xpath_code = "//button[contains(@id,'board-controls-flip')]"
            config_xpath_code = browser.find_element("xpath", config_xpath_code)
            switch_xpath_code = browser.find_element("xpath", switch_xpath_code)
            action_steps = ActionChains(browser)
            action_steps.move_to_element(config_xpath_code).perform()
            switch_xpath_code.click()
            time.sleep(0.1)
            get_screenshot()
            render_value = "index.html"
        case _:
            url = session.get('url')
            if url == None or url == 'None':
                game_code = request.form.get('game-code')
                move_num = request.form.get('move-number')
                url = f"https://www.chess.com/game/live/{game_code}?move={move_num}"
                session['move-number'] = move_num
                session['game-code'] = game_code
                session['url'] = url
                url = session.get('url')
                browser.get(url)
                live_game = get_screenshot()
            else:
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
@app.route('/game-live', methods=['GET', 'POST', 'DELETE'])
def get_image():
    if request.method == 'POST':
        global filename_value
        time.sleep(0.1)
        get_screenshot()
        data = request.get_json()
        filename = data.get("filename")
        os.rename(root, target_root+filename)
        filename_value = "/static/images/"+filename
        #filename_value = target_root+filename
        time.sleep(5)
        return send_file(filename_value, mimetype='image/webp')
    elif request.method == 'DELETE':
        data = request.get_json()
        filename = data.get('filename')
        filename = target_root+filename
        os.remove(filename)
        return jsonify({"message": "Archivo eliminado correctamente."}), 200
    elif request.method == 'GET':
        return jsonify({"filename": filename_value}), 200

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

def get_screenshot():
    try:
        #primero se intenta identificar si es un juego en vivo, buscando el botón de la review  (que aparece en juegos finalizados)
        xpath_code = "//div[contains(@class,'game-review-buttons-component')]"
        web_element_exists = wait_web_element(xpath_code, 10)
        #con esto validamos que si nos paramos en una partida finalizada y no asignamos numero de movimiento, en caso de llegar a la instancia final, cerramos
        #la vista que nos arroja los resultados de la partida.
        if web_element_exists == False:
            raise Exception(f"Unable to locate web element: {xpath_code}")
        xpath_code = "//div[contains(@class,'game-over-modal-content')]//button[contains(@aria-label,'Close')]"
        web_element_exists = wait_web_element(xpath_code, 1)
        if web_element_exists == True: 
            close_end_game_button = browser.find_element(By.XPATH, xpath_code)
            close_end_game_button.click()

        xpath_code = "//wc-chess-board[contains(@id,'board-single') and contains(@class,'board')]"
        board = browser.find_element("xpath", xpath_code)
        board.screenshot('./static/images/ss.webp')
        live_game = False
        #en caso de que tras buscar por 3 segundos, no exista, entendemos que es un juego en vivo
    except TimeoutException:
        xpath_code = "//wc-chess-board[contains(@id,'board-single') and contains(@class,'board')]"
        board = browser.find_element("xpath", xpath_code)
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
    xpath_code = "//a[contains(text(),'ChessCoachSelenium')]"
    web_element_exists = wait_web_element(xpath_code, 10)
    if not web_element_exists: raise Exception(f"Unable to locate web element: {xpath_code}")
        
def set_initial_paths(priv_env):
    global root
    global target_root

    if priv_env == True:
        chess_coach_path = os.path.join(os.path.expanduser("~"), "Chess-Coach")
        root = chess_coach_path+"/app/static/images/ss.webp"
        target_root = chess_coach_path+"/app/static/images/"
        root = root.replace("\\", "/")
        target_root = target_root.replace("\\", "/")
    else:
        root = "C:/Users/bmorales/OneDrive - rmrconsultores.com/Escritorio/Chess-Coach/app/static/images/ss.webp"
        target_root = "C:/Users/bmorales/OneDrive - rmrconsultores.com/Escritorio/Chess-Coach/app/static/images/"

def validate_web_element(xpath):
    web_element = browser.find_elements(By.XPATH, xpath)
    return len(web_element) > 0

def wait_web_element(xpath, time):
    try:
        WebDriverWait(browser, time).until(
            EC.visibility_of_element_located((By.XPATH, xpath))
            )
        return True
    except TimeoutException:
        return False
    
def get_config_file(path):
    global config_data
    with open(path) as config:
        config_data = json.load(config)

def save_config_data(path):
    global config_data
    with open(path, "w") as config:
        json.dump(config_data, config, indent=4)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)