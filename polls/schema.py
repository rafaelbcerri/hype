import graphene

from graphene_mongo import MongoengineObjectType
from polls.models import Question, Choice


class ChoiceType(MongoengineObjectType):
    class Meta:
        model = Choice


class QuestionType(MongoengineObjectType):
    class Meta:
        model = Question


class ChoiceInput(graphene.InputObjectType):
    text = graphene.String(required=True)
    votes = graphene.Int()


class CreateQuestion(graphene.Mutation):
    class Arguments:
        text = graphene.String()
        choices_data = ChoiceInput(required=True)

    question = graphene.Field(lambda: QuestionType)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(self, info, text, choices_data):
        choice = Choice(
            text=choices_data.text,
            votes=choices_data.votes
        )
        question = Question(text=text, choices=[choice])
        question.save()
        ok = True
        return CreateQuestion(question=question, ok=ok)


class MyMutations(graphene.ObjectType):
    create_question = CreateQuestion.Field()


class Query(graphene.ObjectType):
    questions = graphene.List(QuestionType)

    def resolve_questions(self, info):
    	return list(Question.objects.all())


schema = graphene.Schema(query=Query, mutation=MyMutations)
