# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rosters', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='membership',
            old_name='invited_by',
            new_name='approved_by',
        ),
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together=set([('player', 'roster')]),
        ),
    ]
