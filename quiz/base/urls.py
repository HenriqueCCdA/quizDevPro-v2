from django.urls import path

from quiz.base.views import home


urlpatterns = [
    path('', home, name='home'),
]
