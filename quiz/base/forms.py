from django.forms import ModelForm

from quiz.base.models.aluno import Aluno


class AlunoForm(ModelForm):
    class Meta:
        model = Aluno
        fields = ['nome', 'email']
