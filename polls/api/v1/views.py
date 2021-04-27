from django.contrib.auth import get_user_model
from .serializers import QuestionSerializer, CommentSerializer
from rest_framework import generics
from polls.models import Question, Comment

User = get_user_model()


class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class QuestionDetail(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class CommentList(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
