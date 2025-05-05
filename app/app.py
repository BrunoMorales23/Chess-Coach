from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    image = url_for('static', filename='ss.png')
    return render_template('index.html', pic=image)

if __name__ == '__main__':
    app.run(debug=True, port=5000)