import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


class Query(graphene.ObjectType):
    all_users = DjangoListField(UserType)


schema = graphene.Schema(query=Query)
