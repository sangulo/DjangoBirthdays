# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-22 18:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('birthdays', '0002_person_created_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='invitations',
            field=models.ManyToManyField(through='birthdays.Invitation', to='birthdays.Person'),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
