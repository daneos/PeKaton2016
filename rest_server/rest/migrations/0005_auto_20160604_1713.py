# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0004_foodticket'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.TextField()),
                ('user', models.ForeignKey(to='rest.User')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='comments',
            field=models.ManyToManyField(to='rest.Comment'),
        ),
    ]
