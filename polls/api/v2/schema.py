import graphene
from graphene_django import DjangoObjectType
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
    all_questions = graphene.List(QuestionType)

    def resolve_all_questions(self, info):
        return Question.objects.all()


schema = graphene.Schema(query=Query)
