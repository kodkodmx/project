import os
import datetime

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd


# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    investment = 0
    stocks = db.execute(
        "SELECT symbol, SUM(shares) FROM transactions WHERE customer_id == :customer_id GROUP BY symbol", customer_id=session["user_id"])

    # print(stocks)

    for stock in range(len(stocks)):
        # print(stocks[stock-1])
        if stocks[stock-1]['SUM(shares)'] == 0:
            del (stocks[stock-1])

    for row in stocks:
        row['name'] = lookup(row['symbol'])['name']
        row['price'] = lookup(row['symbol'])['price']
        row['total'] = round(lookup(row['symbol'])['price'] * row['SUM(shares)'], 2)
        investment += round(row['total'], 2)

    cash_total = db.execute("SELECT cash FROM users WHERE id == :id", id=session["user_id"])
    cash = round(cash_total[0]['cash'], 2)
    total = round(investment + cash, 2)

    return render_template("index.html", stocks=stocks, investment=investment, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    else:

        if not request.form.get("symbol"):
            return apology("Type a Symbol")

        quote = lookup(request.form.get("symbol"))
        if not quote:
            return apology("Invalid Symbol")

        shares = request.form.get("shares")
        if not shares or shares.isalpha():
            return apology("Invalid Shares")
        else:
            def is_integer(shares):
                try:
                    float(shares)
                except ValueError:
                    return False
                else:
                    return float(shares).is_integer()
            if is_integer(shares) == False:
                return apology("Invalid Shares")
            if int(shares) < 1:
                return apology("Invalid Shares")

        price = quote["price"]
        cost = float(shares) * price

    balance = db.execute("SELECT cash FROM users WHERE id == :id", id=session["user_id"])[0]

    if cost > balance["cash"]:
        return apology("Not Enough Funds")

    else:
        new_cash = float(balance["cash"]) - cost
        now = datetime.datetime.now()
        db.execute("UPDATE users SET cash = :cash WHERE id == :id", cash=new_cash, id=session["user_id"])
        db.execute("INSERT INTO transactions (customer_id, date, type, symbol, shares, price, total) VALUES (:customer_id, :date, :type, :symbol, :shares, :price, :total)",
                   customer_id=session["user_id"], date=now, type="Buy", symbol=request.form.get("symbol"), shares=request.form.get("shares"), price=price, total=cost)
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM transactions WHERE customer_id == :customer_id ORDER BY date DESC", customer_id=session["user_id"])
    for row in transactions:
        row['name'] = lookup(row['symbol'])['name']

    return render_template("history.html", transactions=transactions)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")
    else:
        if not request.form.get("symbol"):
            return apology("Type a Symbol")
        else:
            quote = lookup(request.form.get("symbol"))
            if not quote:
                return apology("Invalid Symbol")
            return render_template("quoted.html", quote=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    else:
        if request.form.get("username") == "" or request.form.get("password") == "" or request.form.get("confirmation") == "":
            return apology("You must fill in all the fields")

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match")

        elif db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username")):
            return apology("Username already taken")

        else:
            username = request.form.get("username")
            password = generate_password_hash(request.form.get("password"))
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password)

            rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]

            # Redirect user to home page
            return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    stocks = db.execute(
        "SELECT symbol, SUM(shares) FROM transactions WHERE customer_id == :customer_id GROUP BY symbol", customer_id=session["user_id"])
    if request.method == "GET":

        for stock in range(len(stocks)):
            # print(stocks[stock-1])
            if stocks[stock-1]['SUM(shares)'] == 0:
                del (stocks[stock-1])

        for row in stocks:
            row['name'] = lookup(row['symbol'])['name']
            row['price'] = lookup(row['symbol'])['price']
            row['total'] = round(lookup(row['symbol'])['price'] * row['SUM(shares)'], 2)

        return render_template("sell.html", stocks=stocks)

    else:
        def is_integer(shares):
            try:
                float(shares)
            except ValueError:
                return False
            else:
                return float(shares).is_integer()

        if request.form.get("shares") != "" and request.form.get("symbol") != "":
            sharescs50 = request.form.get("shares")
            # print(sharescs50)
            sharescs50 = str(sharescs50)
            symbolcs50 = request.form.get("symbol")
            # print(symbolcs50)
            maxshares = db.execute("SELECT SUM(shares) FROM transactions WHERE customer_id == :customer_id AND symbol == :symbol",
                                   customer_id=session["user_id"], symbol=symbolcs50)
            for max in maxshares:
                if sharescs50.isalpha() == True or is_integer(sharescs50) == False or int(sharescs50) < 1 or int(sharescs50) > max['SUM(shares)']:
                    return apology("Invalid Shares")
                else:
                    quote = lookup(symbolcs50)
                    price = quote['price']
                    value = float(sharescs50) * price
                    # print(value)
                    balance = db.execute("SELECT cash FROM users WHERE id == :id", id=session["user_id"])[0]
                    new_cash = float(balance["cash"]) + value
                    # print(new_cash)
                    # print(symbol)
                    now = datetime.datetime.now()
                    db.execute("UPDATE users SET cash = :cash WHERE id == :id", cash=new_cash, id=session["user_id"])
                    db.execute("INSERT INTO transactions (customer_id, date, type, symbol, shares, price, total) VALUES (:customer_id, :date, :type, :symbol, :shares, :price, :total)",
                               customer_id=session["user_id"], date=now, type="Sell", symbol=symbolcs50, shares=-int(sharescs50), price=price, total=value)
                return redirect("/")

        for stock in stocks:
            counter = 0
            shares = request.form.get(stock['symbol'])
            shares == str(shares)
            # print(type(shares))
            if shares != "":
                counter = counter+1
                if shares.isalpha() == True or is_integer(shares) == False or int(shares) < 1 or int(shares) > stock['SUM(shares)']:
                    return apology("Invalid Shares")
            # print(counter)
            # print(stock)
            # print(shares)
            if counter != 0:
                quote = lookup(stock['symbol'])
                price = quote['price']
                value = float(shares) * price
                # print(value)
                balance = db.execute("SELECT cash FROM users WHERE id == :id", id=session["user_id"])[0]
                new_cash = float(balance["cash"]) + value
                # print(new_cash)
                symbol = stock['symbol']
                # print(symbol)
                now = datetime.datetime.now()
                db.execute("UPDATE users SET cash = :cash WHERE id == :id", cash=new_cash, id=session["user_id"])
                db.execute("INSERT INTO transactions (customer_id, date, type, symbol, shares, price, total) VALUES (:customer_id, :date, :type, :symbol, :shares, :price, :total)",
                           customer_id=session["user_id"], date=now, type="Sell", symbol=symbol, shares=-int(shares), price=price, total=value)
                return redirect("/")
            else:
                return apology("Invalid Shares")
    return redirect("/")