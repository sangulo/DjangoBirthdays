# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 18:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dt', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(default='Title', max_length=100)),
                ('invitation_text', models.TextField()),
                ('event_dt', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=9)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birthdays.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(default='', max_length=50)),
                ('birth_dt', models.DateField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='invitation',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='birthdays.Person'),
        ),
    ]
