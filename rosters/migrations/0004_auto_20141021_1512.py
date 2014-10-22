# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rosters', '0003_auto_20141020_1839'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roster',
            name='name',
            field=models.CharField(max_length=255, verbose_name=b'Group name'),
        ),
        migrations.AlterField(
            model_name='roster',
            name='zipcode',
            field=models.CharField(max_length=10, blank=True),
        ),
    ]
