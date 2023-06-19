from flask import Flask, request, jsonify
from src.prompt import ner, people_ner, origin_ner, duration_ner, dates_ner
from flask_cors import CORS, cross_origin
from src.api import minizinc_api

# from train import test
app = Flask(__name__)
CORS(app)


@app.route("/")
def hello():
    user_agent = request.headers.get("User-Agent")
    return "Hello! I see you're using %s" % user_agent


@app.route("/mzn", methods=["POST"])
@cross_origin()
def check_in():
    data = request.get_json(force=True)
    mzc = minizinc_api(data)
    response = jsonify(mzc)
    return response

@app.route("/people/<query>", methods=["GET"])
@cross_origin()
def people(query):
    res = people_ner(query)
    return jsonify(res)

@app.route("/ner/<query>", methods=["GET"])
@cross_origin()
def full(query):
    res = ner(query)
    return jsonify(res)

@app.route("/origin/<query>", methods=["GET"])
@cross_origin()
def origin(query):
    res = origin_ner(query)
    return jsonify(res)

@app.route("/duration/<query>", methods=["GET"])
@cross_origin()
def duration(query):
    res = duration_ner(query)
    return jsonify(res)

@app.route("/dates/<query>", methods=["GET"])
@cross_origin()
def dates(query):
    res = dates_ner(query)
    return jsonify(res)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
