import graphene as gp


class Query(gp.ObjectType):
    nname = gp.NonNull(gp.String)
    ilist = gp.List(gp.String)
    nlist = gp.List(gp.NonNull(gp.String))

    def resolve_nname(self, info):
        return "nome"

    def resolve_ilist(self, info):
        return ["s", "b"]

    def resolve_nlist(self, info):
        return ["s"]


schema = gp.Schema(query=Query)
query = {
    "nname": """
        query {
            nname
        }
    """,
    "ilist": """
        query {
            ilist
        }
    """,
    "nlist": """
        query {
            nlist
        }
    """,
}


if __name__ == "__main__":
    result = schema.execute(query["nname"])
    print("nname = " + str(result.data["nname"]))

    result = schema.execute(query["ilist"])
    print("list = " + str(result.data["ilist"]))

    result = schema.execute(query["nlist"])
    print("nlist = " + str(result.data["nlist"]))
