# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time_start', models.DateTimeField()),
                ('time_end', models.DateTimeField()),
                ('name', models.CharField(max_length=50)),
                ('note', models.TextField()),
                ('place_ext', models.CharField(max_length=200)),
                ('private', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='EventMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('event', models.ForeignKey(to='rest.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='GroupMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group', models.ForeignKey(to='rest.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ParkSpot',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('location', models.CharField(max_length=50)),
                ('free', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time_start', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('session_hash', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('time_start', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('done', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TaskMembership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('role', models.ForeignKey(to='rest.Role')),
                ('task', models.ForeignKey(to='rest.Task')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.AddField(
            model_name='taskmembership',
            name='user',
            field=models.ForeignKey(to='rest.User'),
        ),
        migrations.AddField(
            model_name='task',
            name='members',
            field=models.ManyToManyField(to='rest.User', through='rest.TaskMembership'),
        ),
        migrations.AddField(
            model_name='session',
            name='user',
            field=models.ForeignKey(to='rest.User'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='role',
            field=models.ForeignKey(to='rest.Role'),
        ),
        migrations.AddField(
            model_name='groupmembership',
            name='user',
            field=models.ForeignKey(to='rest.User'),
        ),
        migrations.AddField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(to='rest.User', through='rest.GroupMembership'),
        ),
        migrations.AddField(
            model_name='eventmembership',
            name='role',
            field=models.ForeignKey(to='rest.Role'),
        ),
        migrations.AddField(
            model_name='eventmembership',
            name='user',
            field=models.ForeignKey(to='rest.User'),
        ),
        migrations.AddField(
            model_name='event',
            name='members',
            field=models.ManyToManyField(to='rest.User', through='rest.EventMembership'),
        ),
        migrations.AddField(
            model_name='event',
            name='place_int',
            field=models.ForeignKey(to='rest.Room'),
        ),
    ]
