# Generated by Django 5.1.7 on 2025-03-20 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registros", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="alumno",
            name="apellido_paterno",
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="alumno",
            name="nombre",
            field=models.CharField(max_length=255, null=True),
        ),
    ]
