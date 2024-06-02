#!/usr/bin/python3
"""Runs a flask server for AirBnB_Clone"""

from flask import Flask, render_template
from models import storage
from models.state import State

app = Flask(__name__)


@app.teardown_appcontext
def close_session(exception):
    storage.close()


@app.route("/states_list", strict_slashes=False)
def states():
    """Returns a list of all states in storage"""
    all_states = storage.all(State)
    states = sorted(all_states.values(), key=lambda state: state.name)

    return render_template("7-states_list.html", states=states)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
