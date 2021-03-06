# Generated by Django 4.0.3 on 2022-04-18 10:39

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'verbose_name': 'пользователя', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelOptions(
            name='footerlinks',
            options={'ordering': ('id',), 'verbose_name': 'ссылку футера', 'verbose_name_plural': 'Ссылки футера'},
        ),
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=django.contrib.postgres.fields.citext.CIEmailField(error_messages={'unique': 'Адрес электронной почты уже занят.'}, max_length=255, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=django.contrib.postgres.fields.citext.CICharField(error_messages={'unique': 'Данное имя уже занято. Пожалуйста, выберите другое.'}, max_length=15, unique=True, verbose_name='Username'),
        ),
    ]
