# Generated by Django 4.2 on 2023-04-04 21:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pet",
            old_name="weigth",
            new_name="weight",
        ),
    ]
