import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

from .models import HouseCare


class HouseType(DjangoObjectType):
    class Meta:
        model = HouseCare


class Query(graphene.ObjectType):
    houses = graphene.List(HouseType, search=graphene.String())

    def resolve_houses(self, info):
        return HouseCare.objects.all()


class CreateHouse(graphene.Mutation):

    house = graphene.Field(HouseType)

    class Arguments:
        name = graphene.String(required=True)
        host = graphene.String(required=True)
        address = graphene.String(required=True)
        phone = graphene.String(required=True)

    def mutate(self, info, **kwargs):

        house = HouseCare(**kwargs)
        house.save()
        return CreateHouse(house=house)


class UpdateHouse(graphene.Mutation):
    house = graphene.Field(HouseType)

    class Arguments:
        house_id = graphene.Int(required=True)
        name = graphene.String()
        host = graphene.String()
        address = graphene.String()
        phone = graphene.String()

    def mutate(self, info, house_id, name, host, address, phone):

        house = HouseCare.objects.get(id=house_id)

        house.name = name
        house.host = host
        house.address = address
        house.phone = phone

        house.save()

        return UpdateHouse(house=house)


class DeleteHouse(graphene.Mutation):
    house_id = graphene.Int()

    class Arguments:
        house_id = graphene.Int(required=True)

    def mutate(self, info, house_id):

        house = HouseCare.objects.get(id=house_id)

        house.delete()
        return DeleteHouse(house=house)


class Mutation(graphene.ObjectType):
    create_house = CreateHouse.Field()
    update_house = UpdateHouse.Field()
    delete_house = DeleteHouse.Field()
