# Generated by Django 4.2 on 2023-04-05 02:33

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("groups", "0003_alter_group_pets"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="group",
            name="pets",
        ),
    ]
