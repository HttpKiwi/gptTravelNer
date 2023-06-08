import requests


def minizinc_api(object):
    res = requests.get("http://143.198.177.199:3000/all", json=object)
    return res.json()
