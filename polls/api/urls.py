from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('v1/', include('polls.api.v1.urls')),
    path('v2/', include('polls.api.v2.urls')),

]
