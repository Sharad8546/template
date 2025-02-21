from flask import Flask
from flask import render_template



app=Flask(__name__)

@app.route('/')
def home():

    return render_template("home.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route("/register")
def reg():
    return render_template("register.html")

@app.route("/add_book")
def add_book():
    return render_template("add_book.html")

@app.route("/edit_book")
def edit_book():
    return render_template("edit_book.html")

@app.route("/edit_category")
def edit_category():
    return render_template("edit_category.html")

@app.route("/add_category")
def add_category():
    return render_template("add_category.html")

if __name__=="__main__":
    app.run(debug=True)
