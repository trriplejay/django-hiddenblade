# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import localflavor.us.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('flavor_text', models.CharField(default=b'', max_length=140, blank=True)),
            ],
            options={
                'ordering': ['creation_time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('creation_time', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(default=b'', max_length=255, blank=True)),
                ('player', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['creation_time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField(default=True)),
                ('living_player_list', models.TextField(default=b'', blank=True)),
                ('dead_player_list', models.TextField(default=b'', blank=True)),
                ('house_rules', models.TextField(default=b'No rules defined', help_text=b'Describe any special rules that players of this game should ahere to', blank=True)),
                ('completed', models.BooleanField(default=False)),
                ('cancelled', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('mode', models.CharField(default=b'STD', max_length=3, choices=[(b'STD', b'Standard'), (b'FFA', b'Free For All'), (b'TDM', b'Team Deathmatch'), (b'VIP', b'Protect the VIP'), (b'ZOM', b'Zombie takeover')])),
            ],
            options={
                'ordering': ['start_time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_moderator', models.BooleanField(default=False)),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('invited_by', models.CharField(default=b'', max_length=255)),
                ('games_won', models.SmallIntegerField(default=0)),
                ('frags', models.SmallIntegerField(default=0)),
                ('deaths', models.SmallIntegerField(default=0)),
                ('games_dropped', models.SmallIntegerField(default=0)),
                ('total_games_played', models.SmallIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_approved', models.BooleanField(default=True)),
                ('player', models.ForeignKey(related_name=b'player', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Roster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Group name')),
                ('description', models.TextField(blank=True)),
                ('status', models.CharField(max_length=140, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
                ('state', localflavor.us.models.USStateField(blank=True, max_length=2, choices=[(b'AL', b'Alabama'), (b'AK', b'Alaska'), (b'AS', b'American Samoa'), (b'AZ', b'Arizona'), (b'AR', b'Arkansas'), (b'AA', b'Armed Forces Americas'), (b'AE', b'Armed Forces Europe'), (b'AP', b'Armed Forces Pacific'), (b'CA', b'California'), (b'CO', b'Colorado'), (b'CT', b'Connecticut'), (b'DE', b'Delaware'), (b'DC', b'District of Columbia'), (b'FL', b'Florida'), (b'GA', b'Georgia'), (b'GU', b'Guam'), (b'HI', b'Hawaii'), (b'ID', b'Idaho'), (b'IL', b'Illinois'), (b'IN', b'Indiana'), (b'IA', b'Iowa'), (b'KS', b'Kansas'), (b'KY', b'Kentucky'), (b'LA', b'Louisiana'), (b'ME', b'Maine'), (b'MD', b'Maryland'), (b'MA', b'Massachusetts'), (b'MI', b'Michigan'), (b'MN', b'Minnesota'), (b'MS', b'Mississippi'), (b'MO', b'Missouri'), (b'MT', b'Montana'), (b'NE', b'Nebraska'), (b'NV', b'Nevada'), (b'NH', b'New Hampshire'), (b'NJ', b'New Jersey'), (b'NM', b'New Mexico'), (b'NY', b'New York'), (b'NC', b'North Carolina'), (b'ND', b'North Dakota'), (b'MP', b'Northern Mariana Islands'), (b'OH', b'Ohio'), (b'OK', b'Oklahoma'), (b'OR', b'Oregon'), (b'PA', b'Pennsylvania'), (b'PR', b'Puerto Rico'), (b'RI', b'Rhode Island'), (b'SC', b'South Carolina'), (b'SD', b'South Dakota'), (b'TN', b'Tennessee'), (b'TX', b'Texas'), (b'UT', b'Utah'), (b'VT', b'Vermont'), (b'VI', b'Virgin Islands'), (b'VA', b'Virginia'), (b'WA', b'Washington'), (b'WV', b'West Virginia'), (b'WI', b'Wisconsin'), (b'WY', b'Wyoming')])),
                ('zipcode', models.CharField(max_length=10, blank=True)),
                ('date_created', models.DateField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_public', models.BooleanField(default=False)),
                ('slug', models.SlugField(default=b'', max_length=255, blank=True)),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='rosters.Membership')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='membership',
            name='roster',
            field=models.ForeignKey(to='rosters.Roster'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='game',
            name='roster',
            field=models.ForeignKey(to='rosters.Roster'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='roster',
            field=models.ForeignKey(to='rosters.Roster'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='game',
            field=models.ForeignKey(to='rosters.Game'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='source',
            field=models.ForeignKey(related_name=b'source', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='action',
            name='target',
            field=models.ForeignKey(related_name=b'target', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
