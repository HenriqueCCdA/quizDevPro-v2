from django.db import models

from quiz.base.models import Aluno


class Pergunta(models.Model):
    enunciado = models.TextField()
    disponivel = models.BooleanField(default=False)
    alternativas = models.JSONField()
    alternativas_correta = models.IntegerField(choices=[
        (0, 'A'),
        (1, 'B'),
        (2, 'C'),
        (3, 'D'),
    ])

    def __str__(self):
        return self.enunciado


class Resposta(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE)
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE)
    pontos = models.IntegerField()
    respondida_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['aluno', 'pergunta'], name='resposta_unica')
        ]

    def __str__(self):
        return f'Aluno_id {self.aluno_id} Pergunta_id {self.pergunta_id}'
#       return f'{self.aluno.email} {self.pergunta.enunciado}'
