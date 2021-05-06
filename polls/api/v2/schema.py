import graphene
from graphene_django import DjangoObjectType
from polls.models import Question


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = '__all__'


class Query(graphene.ObjectType):
    all_questions = graphene.List(QuestionType)

    def resolve_all_questions(self,info):
        return Question.objects.all()


schema = graphene.Schema(query=Query)
