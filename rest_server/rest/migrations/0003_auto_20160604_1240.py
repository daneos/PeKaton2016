# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0002_user_password'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomTimetable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('owner', models.ForeignKey(to='rest.User')),
                ('room', models.ForeignKey(to='rest.Room')),
            ],
        ),
        migrations.CreateModel(
            name='TimeSpan',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='UserTimetable',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timespan', models.ForeignKey(to='rest.TimeSpan')),
                ('user', models.ForeignKey(to='rest.User')),
            ],
        ),
        migrations.AddField(
            model_name='roomtimetable',
            name='timespan',
            field=models.ForeignKey(to='rest.TimeSpan'),
        ),
        migrations.AddField(
            model_name='room',
            name='timetable',
            field=models.ManyToManyField(to='rest.TimeSpan', through='rest.RoomTimetable'),
        ),
    ]
