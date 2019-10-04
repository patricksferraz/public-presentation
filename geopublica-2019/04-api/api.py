# -*- coding: utf-8 -*-
"""
Exemplo de utilização do GraphQL com Flask (protocolo HTTP)
"""


"""
IMPORTAÇÕES DE BIBLIOTECAS
"""


from flask import Flask, jsonify
from flask_graphql import GraphQLView
from db.postgres import Postgres
from graphene import ObjectType, Int, String, List, Schema


"""
INICIALIZAÇÃO DA API E CONEXÃO COM POSTGRES
"""


app = Flask(__name__)
app.debug = True
post = Postgres()


"""
SCHEMAS
"""


class Place(ObjectType):
    cep = Int(required=True)
    id_state = Int(required=True)
    id_city = Int(required=True)
    district = String(required=True)
    public_place = String(required=True)


class City(ObjectType):
    id = Int(required=True)
    id_state = Int(required=True)
    name = String(required=True)
    places = List(Place)


class State(ObjectType):
    id = Int(required=True)
    name = String(required=True)
    acronym = String(required=True)
    cities = List(City)


"""
FUNÇÕES PARA FORMATAÇÃO DA ESTRUTURA DE RETORNO
"""


def _format_n0(tuple: list):
    state = State(id=tuple[0], name=tuple[1], acronym=tuple[2])

    if len(tuple) > 3:
        state.cities = list(map(_format_n1, tuple[3]))

    return state


def _format_n1(tuple: list):
    city = City(id=tuple[0], id_state=tuple[1], name=tuple[2])

    if len(tuple) > 3:
        city.places = list(map(_format_n2, tuple[3].split(";")))

    return city


def _format_n2(tuple: list):
    tuple = tuple.split(",")

    place = Place(
        cep=tuple[0],
        id_state=tuple[1],
        id_city=tuple[2],
        district=tuple[3],
        public_place=tuple[4],
    )

    return place


def state_format(states: list) -> list:
    """Return all states formated as a dictionary

    Arguments:
        states {list} -- List of states retuned of database

    Returns:
        list -- states formated
    """
    return list(map(_format_n0, states))


"""
QUERY
"""


class Query(ObjectType):
    get_address = List(
        State,
        state=String(default_value="%"),
        city=String(default_value="%"),
        place=String(default_value="%"),
        limit=Int(default_value=10),
        page=Int(default_value=0),
    )

    def resolve_get_address(_, info, state, city, place, limit, page):
        places = post.get_place(
            {"state": state, "city": city, "place": place}, limit, page
        )
        return state_format(places)


"""
ENCAPSULANDO
"""


schema = Schema(query=Query)


"""
DEFININDO ROTAS EM URL
"""


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql",
        schema=schema,
        graphiql=True,  # for having the GraphiQL interface
    ),
)


@app.route("/")
def index():
    return jsonify(
        api_name="graphql-address", version="1.0", author="Patrick Ferraz"
    )
