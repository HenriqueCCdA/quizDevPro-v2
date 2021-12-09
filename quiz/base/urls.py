from django.urls import path

from quiz.base import views

app_name = 'base'
urlpatterns = [
    path('', views.home, name='home'),
    path('pergunta/<int:indice>', views.pergunta, name='pergunta'),
    path('classificacao/', views.classificacao, name='classificacao'),
]
