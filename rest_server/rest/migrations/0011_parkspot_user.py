# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0010_auto_20160604_2225'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkspot',
            name='user',
            field=models.ForeignKey(blank=True, to='rest.User', null=True),
        ),
    ]
