# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0007_user_points_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='place_ext',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='place_int',
            field=models.ForeignKey(blank=True, to='rest.Room', null=True),
        ),
    ]
