import graphene

from graphene_mongo import MongoengineObjectType
from api.models.thing import Thing as ThingModel


class ThingType(MongoengineObjectType):
  class Meta:
    model = ThingModel


class CreateThing(graphene.Mutation):
  class Arguments:
    text = graphene.String(required=True)
    sub_things = graphene.List(graphene.String)

  thing = graphene.Field(lambda: ThingType)
  ok = graphene.Boolean()

  @staticmethod
  def mutate(self, info, text, **args):
    sub_things = args.get('sub_things')
    thing = ThingModel(text=text, sub_things=sub_things)
    thing.save()

    return CreateThing(thing=thing, ok=True)


class UpdateThing(graphene.Mutation):
  class Arguments:
    id = graphene.String(required=True)
    text = graphene.String()
    sub_things = graphene.List(graphene.String)

  thing = graphene.Field(lambda: ThingType)
  ok = graphene.Boolean()

  @staticmethod
  def mutate(self, info, id, **args):
    thing = ThingModel.objects.get(id=id)

    text = args.get('text')
    sub_things = args.get('sub_things')

    if text: thing.text = text
    if sub_things: thing.sub_things = sub_things

    if text or sub_things: thing.save()

    return UpdateThing(thing=thing, ok=True)


class DeleteThing(graphene.Mutation):
  class Arguments:
    id = graphene.String(required=True)

  ok = graphene.Boolean()

  @staticmethod
  def mutate(self, info, id):
    thing = ThingModel.objects.get(id=id)
    thing.delete()

    return DeleteThing(ok=True)


class Query(graphene.ObjectType):
  things = graphene.List(ThingType)

  def resolve_things(self, info):
    return list(ThingModel.objects.all())


class Mutation(graphene.ObjectType):
  create_thing = CreateThing.Field()
  update_thing = UpdateThing.Field()
  delete_thing = DeleteThing.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
