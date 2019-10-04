import utils as u
import requests
import json

URL = "http://127.0.0.1:5000/graphql"
LIMIT = 20000
headers = u.HEADERS
payload = {
    "local_min": """
        query {
            getState(limit:20000) {
                name
            }
        }
    """,
    "local_med": """
        query {
            getState(limit:20000) {
                name
                acronym
            }
        }
    """,
    "local_max": """
        query {
            getState(limit:20000) {
                id
                name
                acronym
            }
        }
    """,
    "border_min": """
        query {
            getState(limit:20000) {
                name
                cities {
                    name
                }
            }
        }
    """,
    "border_med": """
        query {
            getState(limit:20000) {
                name
                cities {
                    id
                    name
                }
            }
        }
    """,
    "border_max": """
        query {
            getState(limit:20000) {
                id
                name
                acronym
                cities {
                    id
                    idState
                    name
                }
            }
        }
    """,
    "global_min": """
        query {
            getState(limit:20000) {
                acronym
                cities {
                    name
                    places {
                        cep
                    }
                }
            }
        }
    """,
    "global_med": """
        query {
            getState(limit:20000) {
                id
                name
                acronym
                cities {
                    id
                    name
                    places {
                        cep
                        district
                    }
                }
            }
        }
    """,
    "global_max": """
        query {
            getState(limit:20000) {
                id
                name
                acronym
                cities {
                    id
                    idState
                    name
                    places {
                        cep
                        idState
                        idCity
                        district
                        publicPlace
                    }
                }
            }
        }
    """,
}


# STATE
def req_local_scope_min():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["local_min"]}
    )


def req_local_scope_med():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["local_med"]}
    )


def req_local_scope_max():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["local_max"]}
    )


# CITY
def req_border_scope_min():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["border_min"]}
    )


def req_border_scope_med():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["border_med"]}
    )


def req_border_scope_max():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["border_max"]}
    )


# PLACE
def req_global_scope_min():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["global_min"]}
    )


def req_global_scope_med():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["global_med"]}
    )


def req_global_scope_max():
    requests.post(
        f"{URL}", headers=headers, json={"query": payload["global_max"]}
    )


request = [
    {
        "url": URL,
        "function": req_local_scope_min,
        "payload": payload["local_min"],
        "scope": "local",
        "blockSize": "min",
    },
    {
        "url": URL,
        "function": req_local_scope_med,
        "payload": payload["local_med"],
        "scope": "local",
        "blockSize": "med",
    },
    {
        "url": URL,
        "function": req_local_scope_max,
        "payload": payload["local_max"],
        "scope": "local",
        "blockSize": "max",
    },
    {
        "url": URL,
        "function": req_border_scope_min,
        "payload": payload["border_min"],
        "scope": "border",
        "blockSize": "min",
    },
    {
        "url": URL,
        "function": req_border_scope_med,
        "payload": payload["border_med"],
        "scope": "border",
        "blockSize": "med",
    },
    {
        "url": URL,
        "function": req_border_scope_max,
        "payload": payload["border_max"],
        "scope": "border",
        "blockSize": "max",
    },
    {
        "url": URL,
        "function": req_global_scope_min,
        "payload": payload["global_min"],
        "scope": "global",
        "blockSize": "min",
    },
    {
        "url": URL,
        "function": req_global_scope_med,
        "payload": payload["global_med"],
        "scope": "global",
        "blockSize": "med",
    },
    {
        "url": URL,
        "function": req_global_scope_max,
        "payload": payload["global_max"],
        "scope": "global",
        "blockSize": "max",
    },
]

response = []
out = open("out/log_test_graphql.out.json", "w")
for r in u._exec(request, 1):
    response.append(r)
out.write(json.dumps(response))
