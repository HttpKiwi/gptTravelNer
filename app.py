from flask import Flask, request, jsonify
from src.prompt import ner
from flask_cors import CORS
from src.api import minizinc_api

# from train import test
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
users_seen = {}


@app.route("/")
def hello():
    user_agent = request.headers.get("User-Agent")
    return "Hello! I see you're using %s" % user_agent


@app.route("/test/<query>", methods=["GET"])
def test(query):
    res = ner(query)
    return jsonify(res)


@app.route("/<query>", methods=["GET"])
def check_in(query):
    res = ner(query)
    mzc = minizinc_api(res)
    return jsonify(mzc)


if __name__ == "__main__":
    app.run()
