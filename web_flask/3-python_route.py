#!/usr/bin/python3
"""Runs a Flask web app"""

from flask import Flask
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
