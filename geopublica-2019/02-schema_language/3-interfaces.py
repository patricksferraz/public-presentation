import graphene as gp


class PublicPlace(gp.Interface):
    id = gp.ID(required=True)
    name = gp.String(required=True)
    address = gp.String(required=True)


class Urban(gp.ObjectType):
    class Meta:
        interfaces = (PublicPlace,)


class Rural(gp.ObjectType):
    class Meta:
        interfaces = (PublicPlace,)

    production = gp.String()


class Query(gp.ObjectType):
    address = gp.Field(PublicPlace, required=True, tp=gp.Int(required=True))

    def resolve_address(_, info, tp):
        if tp == 1:
            return Urban(name="AGERBA")
        return Rural(name="Fazenda Seu Chico")


schema = gp.Schema(query=Query, types=[Urban, Rural])
query = """
    query {
        address(tp: 1) {
            name
        }
    }
"""


if __name__ == "__main__":
    # annotation: inline-fragments
    result = schema.execute(query)
    print(result.data)
