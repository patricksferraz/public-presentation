import graphene


class GeoInput(graphene.InputObjectType):
    lat = graphene.Float(required=True)
    lng = graphene.Float(required=True)

    @property
    def latlng(self):
        return "({},{})".format(self.lat, self.lng)


class Address(graphene.ObjectType):
    latlng = graphene.String()


class Query(graphene.ObjectType):
    address = graphene.Field(Address, geo=GeoInput(required=True))

    def resolve_address(self, info, geo):
        return Address(latlng=geo.latlng)


schema = graphene.Schema(query=Query)
query = """
    query something{
      address(geo: {lat:32.2, lng:12}) {
        latlng
      }
    }
"""


if __name__ == "__main__":
    result = schema.execute(query)
    print(result.data)
