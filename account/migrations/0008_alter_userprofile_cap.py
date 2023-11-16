# Generated by Django 4.2.6 on 2023-11-16 09:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_userprofile_cap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cap',
            field=models.CharField(blank=True, max_length=5, null=True, validators=[django.core.validators.RegexValidator(message='Inserisci un CAP valido', regex='^[0-9]{5}')], verbose_name='C.A.P.'),
        ),
    ]
