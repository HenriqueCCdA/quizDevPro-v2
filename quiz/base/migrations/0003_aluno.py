# Generated by Django 3.2.9 on 2021-12-01 03:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_pergunta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Aluno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=64)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('criado_em', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
