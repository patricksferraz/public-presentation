import graphene as gp


class Urban(gp.ObjectType):
    name = gp.String()
    number = gp.String()


class Rural(gp.ObjectType):
    name = gp.String()
    production = gp.String()


class Other(gp.ObjectType):
    name = gp.String()
    depth = gp.Float()


class SearchResult(gp.Union):
    class Meta:
        types = (Urban, Rural, Other)


class Query(gp.ObjectType):
    result = gp.Field(SearchResult, required=True, tp=gp.Int(required=True))

    def resolve_result(_, info, tp):
        if tp == 1:
            return Urban(name="AGERBA")
        elif tp == 2:
            return Rural(name="Fazenda Seu Chico")
        else:
            return Other(name="Submarino P5300TR")


schema = gp.Schema(query=Query)
query = """
    query {
        result(tp: 2) {
            ... on Rural {
                name
            }
        }
    }
"""


if __name__ == "__main__":
    result = schema.execute(query)
    print(result.data)
