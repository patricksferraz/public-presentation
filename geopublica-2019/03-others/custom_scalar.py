import graphene as gp
import datetime
from graphene.types import Scalar
from graphql.language import ast


class DateTime(Scalar):
    # Request
    @staticmethod
    def serialize(dt):
        return dt.isoformat()

    # Query variables
    @staticmethod
    def parse_literal(node):
        if isinstance(node, ast.StringValue):
            return datetime.datetime.strptime(
                node.value, "%Y-%m-%dT%H:%M:%S.%f"
            )

    # Query content
    @staticmethod
    def parse_value(value):
        return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")


class Person(gp.ObjectType):
    data_nascimento = DateTime()


schema = gp.Schema(query=Person)
