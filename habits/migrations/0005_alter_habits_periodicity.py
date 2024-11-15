# Generated by Django 5.1.2 on 2024-11-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0004_habits_next_reminde"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habits",
            name="periodicity",
            field=models.CharField(
                choices=[
                    ("Everyday", "каждый день"),
                    ("Once every two days", "раз в два дня"),
                    ("Once every three days", "раз в три дня"),
                    ("Once every four days", "раз в четыре дня"),
                    ("Once every five days", "раз в пять дней"),
                    ("Once every six days", "раз в шесть дней"),
                    ("Weekly", "раз в неделю"),
                ],
                default="EVERYDAY",
                max_length=50,
                verbose_name="Периодичность",
            ),
        ),
    ]
