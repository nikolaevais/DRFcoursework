# Generated by Django 5.1.2 on 2024-10-27 07:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Habits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=250, verbose_name='Место')),
                ('times', models.TimeField(verbose_name='Время, когда необходимо выполнить привычку')),
                ('move', models.CharField(max_length=250, verbose_name='Действие')),
                ('is_sign_of_pleasant_habit', models.BooleanField(default=False, verbose_name='Признак приятной привычки')),
                ('periodicity', models.CharField(choices=[('EVERYDAY', 'каждый день'), ('EVERYWEEK', 'раз в неделю')], default='EVERYDAY', max_length=50, verbose_name='Периодичность')),
                ('reward', models.CharField(blank=True, max_length=250, null=True, verbose_name='Вознаграждение')),
                ('time_to_complete', models.TimeField(blank=True, null=True, verbose_name='Время на выполнение привычки')),
                ('is_public', models.BooleanField(default=False, verbose_name='Видно всем')),
                ('related_habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='habits.habits', verbose_name='Связанная привычка')),
            ],
            options={
                'verbose_name': 'Привычка',
                'verbose_name_plural': 'Привычки',
            },
        ),
    ]