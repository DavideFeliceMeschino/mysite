# Generated by Django 4.2.6 on 2023-11-16 09:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_alter_userprofile_cap'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cf',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message='Inserisci un codice fiscale valido', regex='^[A-Z]{6}[0-9]{2}[A-Z]{1}[0-9]{2}[A-Z]{1}[0-9]{3}[A-Z]{1}$')], verbose_name='Codice Fiscale'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='cap',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(message='Inserisci un CAP valido', regex='^[0-9]{5}$')], verbose_name='C.A.P.'),
        ),
    ]
