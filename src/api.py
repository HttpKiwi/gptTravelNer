import requests


def minizinc_api(object):
    res = requests.get("http:/143.198.177.199:3666/all", json=object)
    return res.json()
