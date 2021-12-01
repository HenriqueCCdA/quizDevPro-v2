from django.contrib import admin

from quiz.base.models import Pergunta


@admin.register(Pergunta)
class PeguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado', 'disponivel')