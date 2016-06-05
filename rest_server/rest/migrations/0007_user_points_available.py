# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0006_auto_20160604_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='points_available',
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
    ]
