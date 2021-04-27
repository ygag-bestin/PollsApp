from django.urls import path, include
from . import views

urlpatterns = [
    path('questions/', views.QuestionList.as_view()),
    path('questions/<int:pk>/',
         views.QuestionDetail.as_view()),
    path('comments/', views.CommentList.as_view()),

]
