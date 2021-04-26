from django.contrib.auth import get_user_model
from .serializers import QuestionSerializer
from rest_framework import generics
from polls.models import Question

User = get_user_model()


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
