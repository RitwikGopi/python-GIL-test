from flask import Flask, jsonify, request

from main import loop

app = Flask(__name__)


@app.route("/loop", methods=["POST"])
def perform():
    numbers = request.get_json()
    return loop(numbers)
