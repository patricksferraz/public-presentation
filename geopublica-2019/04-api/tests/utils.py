import requests
import timeit

REPEAT = 100
HEADERS = {"content-type": "application/json"}


def _get(url, payload=None):
    r = requests.get(url, headers=HEADERS)
    return {"size": r.headers["Content-Length"], "content": r.json()}


def _post(url, payload):
    r = requests.post(url, headers=HEADERS, json={"query": payload})
    return {"size": r.headers["Content-Length"], "content": r.json()}


func = [_get, _post]


def _exec(operations, set):
    for o in operations:
        r = func[set](o["url"], o["payload"])
        time = timeit.repeat(o["function"], repeat=REPEAT, number=1)
        yield {
            "scope": o["scope"],
            "blockSize": o["blockSize"],
            "size": r["size"],
            "time": time,
        }
