# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rosters', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roster',
            name='city',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='roster',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='roster',
            name='status',
            field=models.CharField(max_length=140, blank=True),
        ),
    ]
