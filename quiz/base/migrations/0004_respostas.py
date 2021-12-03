# Generated by Django 3.2.9 on 2021-12-03 05:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_aluno'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resposta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pontos', models.IntegerField()),
                ('respondida_em', models.DateTimeField(auto_now_add=True)),
                ('aluno', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.aluno')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.pergunta')),
            ],
        ),
        migrations.AddConstraint(
            model_name='resposta',
            constraint=models.UniqueConstraint(fields=('aluno', 'pergunta'), name='resposta_unica'),
        ),
    ]