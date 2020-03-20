import graphene
from graphene_django import DjangoObjectType

from .models import Track


class SermonType(DjangoObjectType):
    class Meta:
        model = Track


class Query(graphene.ObjectType):
    sermons = graphene.List(SermonType, search=graphene.String())

    def resolve_sermons(self, info):
        return Track.objects.all()


class CreateSermon(graphene.Mutation):

    sermon = graphene.Field(SermonType)

    class Arguments:
        title = graphene.String(required=True)
        url = graphene.String(required=True)
        created_by = graphene.String(required=True)

    def mutate(self, info, **kwargs):

        sermon = Track(**kwargs)
        sermon.save()
        return CreateSermon(sermon=sermon)


class UpdateSermon(graphene.Mutation):
    sermon = graphene.Field(SermonType)

    class Arguments:
        sermon_id = graphene.Int(required=True)
        title = graphene.String()
        url = graphene.String()
        created_by = graphene.String()

    def mutate(self, info, sermon_id, title, url, created_by):

        sermon = Track.objects.get(id=sermon_id)

        sermon.title = title
        sermon.url = url
        sermon.created_by = created_by

        sermon.save()

        return UpdateSermon(sermon=sermon)


class DeleteSermon(graphene.Mutation):
    sermon_id = graphene.Int()

    class Arguments:
        sermon_id = graphene.Int(required=True)

    def mutate(self, info, sermon_id):

        sermon = Track.objects.get(id=sermon_id)

        sermon.delete()
        return DeleteSermon(sermon=sermon)


class Mutation(graphene.ObjectType):
    create_sermon = CreateSermon.Field()
    update_sermon = UpdateSermon.Field()
    delete_sermon = DeleteSermon.Field()
