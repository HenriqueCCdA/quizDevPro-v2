from django.contrib import admin

from quiz.base.models import Pergunta, Resposta


@admin.register(Pergunta)
class PeguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'enunciado', 'disponivel')


@admin.register(Resposta)
class RepostasAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'aluno_id', 'pergunta', 'pergunta_id', 'pontos', 'respondida_em')
