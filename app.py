from flask import Flask, request, jsonify
from src.prompt import ner
from flask_cors import CORS, cross_origin
from src.api import minizinc_api

# from train import test
app = Flask(__name__)
CORS(app)

users_seen = {}


@app.route("/")
def hello():
    user_agent = request.headers.get("User-Agent")
    return "Hello! I see you're using %s" % user_agent


@app.route("/mnz/", methods=["GET"])
@cross_origin()
def check_in(extratedObejct):
    mzc = minizinc_api(extratedObejct)
    response = jsonify(mzc)
    return response


@app.route("/ner/<query>", methods=["GET"])
@cross_origin()
def test(query):
    res = ner(query)
    response = jsonify(res)
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
