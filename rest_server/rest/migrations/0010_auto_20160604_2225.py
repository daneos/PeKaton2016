# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0009_auto_20160604_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.ForeignKey(to='rest.EventType'),
        ),
    ]
