# Generated by Django 4.2.6 on 2023-11-15 09:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codice', models.CharField(max_length=50, unique=True)),
                ('valido_da', models.DateTimeField()),
                ('valido_a', models.DateTimeField()),
                ('sconto', models.IntegerField(help_text='Percentuale compresa tra 0 e 100', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('attivo', models.BooleanField()),
            ],
        ),
    ]