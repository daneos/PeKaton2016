# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0005_auto_20160604_1713'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='hour_goal',
            field=models.FloatField(default=160),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='hours',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='points',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.FloatField(default=4000),
            preserve_default=False,
        ),
    ]
