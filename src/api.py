import requests


def minizinc_api(object):
    res = requests.get("http://127.0.0.1:3000/all", json=object)
    return res.json()
