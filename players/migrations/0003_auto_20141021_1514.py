# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0002_auto_20141021_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='home_zip',
            field=models.CharField(max_length=10, verbose_name=b'Home zipcode', blank=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='work_zip',
            field=models.CharField(max_length=10, verbose_name=b'Work zipcode', blank=True),
        ),
    ]
