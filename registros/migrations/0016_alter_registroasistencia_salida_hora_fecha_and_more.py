# Generated by Django 5.1.7 on 2025-04-11 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("registros", "0015_alter_registroasistencia_salida_registrada"),
    ]

    operations = [
        migrations.AlterField(
            model_name="registroasistencia",
            name="salida_hora_fecha",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="registroasistencia",
            name="salida_registrada",
            field=models.BooleanField(default=False),
        ),
    ]
