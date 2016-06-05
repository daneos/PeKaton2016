# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0011_parkspot_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('from_user_id', models.IntegerField()),
                ('to_user_id', models.IntegerField()),
                ('time', models.DateTimeField()),
                ('text', models.TextField()),
            ],
        ),
    ]
