from flask import Flask, flash, redirect, render_template, request, url_for
from helpers import apology
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

bootstrap = Bootstrap5(app)

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/book')
def airbnb():
    return render_template('book.html')

if __name__ == '__main__':
    app.run()