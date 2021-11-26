import pytest
from model_bakery import baker
from quiz.base.models import Pergunta


@pytest.fixture
def questions(db):
    return baker.make(Pergunta, 3)


def test_models_pergunta(questions):

    for question, question_db in zip(questions, Pergunta.objects.all()):
        assert question.enunciado == question_db.enunciado
        assert question.disponivel == question_db.disponivel
        assert question.alternativas == question_db.alternativas
        assert question.alternativas_correta == question_db.alternativas_correta
