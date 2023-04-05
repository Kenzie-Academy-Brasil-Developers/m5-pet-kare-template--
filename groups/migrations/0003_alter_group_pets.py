# Generated by Django 4.2 on 2023-04-05 02:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("pets", "0003_remove_pet_group"),
        ("groups", "0002_group_pets"),
    ]

    operations = [
        migrations.AlterField(
            model_name="group",
            name="pets",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="group",
                to="pets.pet",
            ),
        ),
    ]