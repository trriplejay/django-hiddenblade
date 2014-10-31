# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rosters', '0002_auto_20141029_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='action',
            name='roster',
            field=models.ForeignKey(default=1, to='rosters.Roster'),
            preserve_default=False,
        ),
    ]
