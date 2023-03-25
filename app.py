from flask import Flask, flash, redirect, render_template, request, url_for
from helpers import apology
from flask_bootstrap import Bootstrap5

app = Flask(__name__)    

bootstrap = Bootstrap5(app)

@app.route("/", methods=["GET", "POST"] )
def index():
    if request.method == "GET":
        return render_template('index.html')
    else:
        value = request.form.get("info")
        if value == "do":
            return render_template('index.html', selection = "do")
        
        elif value == "meet":
            return render_template('index.html', selection = "meet")
        
        elif value == "be":
            return render_template('index.html', selection = "be")
        
        elif value == "host":
            return render_template('index.html', selection = "host")

@app.route('/book')
def airbnb():
    return render_template('book.html')

@app.route('/rev')
def rev():
    return render_template('reviews.html')

@app.route('/insta')
def insta():
    return render_template('insta.html')

if __name__ == '__main__':
    app.run()

