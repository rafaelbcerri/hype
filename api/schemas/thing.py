import graphene

from graphene_mongo import MongoengineObjectType
from api.models.thing import Thing as ThingModel

class ThingType(MongoengineObjectType):
  class Meta:
    model = ThingModel


class CreateThing(graphene.Mutation):
  class Arguments:
    text = graphene.String()
    sub_things = graphene.List(graphene.String)

  thing = graphene.Field(lambda: ThingType)
  ok = graphene.Boolean()

  @staticmethod
  def mutate(self, info, text, sub_things):
    thing = ThingModel(text=text, sub_things=sub_things)
    thing.save()

    return CreateThing(thing=thing, ok=True)


class Query(graphene.ObjectType):
  things = graphene.List(ThingType)

  def resolve_things(self, info):
    return list(ThingModel.objects.all())


class Mutation(graphene.ObjectType):
  create_thing = CreateThing.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
