import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField
from polls.models import Question, Choice


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = ['choice_text', 'votes']


class QuestionType(DjangoObjectType):
    choice = ChoiceType()

    class Meta:
        model = Question
        fields = '__all__'


class Query(graphene.ObjectType):
    all_questions = DjangoListField(QuestionType)


schema = graphene.Schema(query=Query)
