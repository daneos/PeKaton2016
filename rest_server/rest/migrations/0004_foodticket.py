# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0003_auto_20160604_1240'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodTicket',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('code', models.CharField(max_length=50)),
                ('thumb', models.URLField()),
            ],
        ),
    ]
