# Generated by Django 3.0.8 on 2024-02-22 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cm', models.CharField(max_length=8)),
                ('retranca', models.CharField(max_length=100)),
                ('duracao', models.IntegerField()),
                ('tipo', models.CharField(max_length=2)),
                ('cliente', models.CharField(max_length=100)),
                ('choques', models.CharField(max_length=100)),
                ('exibicao', models.CharField(max_length=1)),
                ('data', models.CharField(max_length=10)),
                ('pt', models.CharField(max_length=5)),
                ('programa', models.CharField(max_length=100)),
            ],
        ),
    ]
