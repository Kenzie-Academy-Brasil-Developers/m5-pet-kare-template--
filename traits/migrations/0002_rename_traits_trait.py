# Generated by Django 4.2 on 2023-04-07 20:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0002_rename_pets_pet"),
        ("traits", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Traits",
            new_name="Trait",
        ),
    ]
