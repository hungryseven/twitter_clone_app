# Generated by Django 4.0.3 on 2022-05-29 16:42

import authorization.models
import django.contrib.postgres.fields.citext
import django.core.validators
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0005_notifications'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=django.contrib.postgres.fields.citext.CICharField(error_messages={'unique': 'Данное имя уже занято. Пожалуйста, выберите другое.'}, max_length=15, unique=True, validators=[django.core.validators.MinLengthValidator(4, 'Имя пользователя не может быть менее 4 символов.'), authorization.models.validate_username], verbose_name='Username'),
        ),
    ]
