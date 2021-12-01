from django.db import models


class Aluno(models.Model):
    nome = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
