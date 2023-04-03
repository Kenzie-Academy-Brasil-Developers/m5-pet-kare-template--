# Generated by Django 4.1.7 on 2023-04-03 14:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0001_initial"),
        ("traits", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trait",
            name="pet",
            field=models.ManyToManyField(related_name="traits", to="pets.pet"),
        ),
    ]
