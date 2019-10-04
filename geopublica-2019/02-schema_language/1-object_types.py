# annotation (argument)

import graphene as gp


# meta class (name)
class Query(gp.ObjectType):
    # annotation (resolver)
    state = gp.String()

    def resolve_state(_, info):
        return "Bahia"


# arguments (query, mutations, types, auto_camelcase)
schema = gp.Schema(query=Query)
query = """
    query {
        state
    }
"""


if __name__ == "__main__":
    result = schema.execute(query)
    print(result.data)
