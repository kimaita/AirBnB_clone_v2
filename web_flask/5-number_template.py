#!/usr/bin/python3
"""Runs a Flask web app"""

from flask import Flask, render_template
from markupsafe import escape

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    """Returns a hello text"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Returns hbnb"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    """Returns a description of C"""
    text = text.replace("_", " ")
    return f"C {escape(text)}"


@app.route("/python", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text):
    """Returns a description of Python"""
    text = text.replace("_", " ")
    return f"Python {escape(text)}"


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """Prints n if it is an integer"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Renders n in HTML if it is an integer"""
    return render_template('5-number.html', number=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
