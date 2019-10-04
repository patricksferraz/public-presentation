import graphene


class Address(graphene.ObjectType):
    street = graphene.String()
    number = graphene.Int()


class CreateAddress(graphene.Mutation):
    # arguments that mutation needs for resolving
    class Arguments:
        street = graphene.String()
        number = graphene.Int(default_value=440)

    # output fields
    ok = graphene.Boolean()
    address = graphene.Field(Address)

    def mutate(self, info, street, number):
        address = Address(street=street, number=number)
        ok = True
        return CreateAddress(address=address, ok=ok)


class Mutations(graphene.ObjectType):
    create_address = CreateAddress.Field()


schema = graphene.Schema(mutation=Mutations)
query = """
    mutation {
        createAddress(street:"Avenida Luís Viana Filho") {
            address {
                street
            }
            ok
        }
    }
"""


if __name__ == "__main__":
    result = schema.execute(query)
    print(result.data)
