from django.urls import path

from quiz.base.views import home, pergunta

app_name = 'base'
urlpatterns = [
    path('', home, name='home'),
    path('pergunta/<slug:slug>', pergunta, name='pergunta'),
]
