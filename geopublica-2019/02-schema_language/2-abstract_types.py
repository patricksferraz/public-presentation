import graphene as gp


class StateFields(gp.AbstractType):
    name = gp.String()

    def resolve_name(_, info):
        return "Bahia"


class State(gp.ObjectType, StateFields):
    pass


class Query(gp.ObjectType):
    state = gp.Field(State)

    def resolve_state(_, info):
        return State()


schema = gp.Schema(query=Query)
query = """
    query {
        state {
            name
        }
    }
"""


if __name__ == "__main__":
    result = schema.execute(query)
    print(result.data)
