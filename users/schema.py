from django.contrib.auth.models import User
import graphene
from graphene_django import DjangoObjectType


class AuthorType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    author = graphene.Field(AuthorType, id=graphene.Int(required=True))
    me = graphene.Field(AuthorType)
    authors = graphene.List(AuthorType)

    def resolve_author(self, info, id):
        return User.objects.get(id=id)

    def resolve_authors(self, info):
        return User.objects.all()

    def resolve_me(self, info):
        author = info.context.user
        if author.is_anonymous:
            raise Exception("You are not logged in")

        return author


class CreateAuthor(graphene.Mutation):
    author = graphene.Field(AuthorType)

    class Arguments:
        first_name = graphene.String()
        last_name = graphene.String()
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, username, email, password, first_name, last_name):
        author = User(username=username, email=email,
                      last_name=last_name, first_name=first_name)
        author.set_password(password)
        author.save()
        return CreateAuthor(author=author)


class Mutation(graphene.ObjectType):
    create_author = CreateAuthor.Field()
