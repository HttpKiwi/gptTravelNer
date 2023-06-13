from flask import Flask, request, jsonify
from src.prompt import ner
from flask_cors import CORS, cross_origin
from src.api import minizinc_api

# from train import test
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
users_seen = {}


@app.route("/")
def hello():
    user_agent = request.headers.get("User-Agent")
    return "Hello! I see you're using %s" % user_agent


@app.route("/ner/<query>", methods=["GET"])
@cross_origin()
def test(query):
    res = ner(query)
    return jsonify(res)


CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/<query>", methods=["GET"])
@cross_origin()
def check_in(query):
    res = ner(query)
    mzc = minizinc_api(res)
    return jsonify(mzc)


if __name__ == "__main__":
    app.run(debug=True)
