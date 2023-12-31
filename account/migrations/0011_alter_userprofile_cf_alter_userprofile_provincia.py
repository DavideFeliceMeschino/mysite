# Generated by Django 4.2.6 on 2023-11-16 10:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_alter_userprofile_provincia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cf',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message='Inserisci un codice fiscale valido', regex='^[A-Za-z]{6}[0-9]{2}[A-Za-z]{1}[0-9]{2}[A-Za-z]{1}[0-9]{3}[A-Za-z]{1}$')], verbose_name='Codice Fiscale'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='provincia',
            field=models.CharField(blank=True, choices=[('Latina', 'LT'), ('Roma', 'RM'), ('Milano', 'MI')], default=None, max_length=100, null=True, verbose_name='Provincia'),
        ),
    ]
