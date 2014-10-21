from django.db import models
from players.models import Player
from localflavor.us.models import USPostalCodeField
from localflavor.us.models import USStateField
from django.template.defaultfilters import slugify


# Create your models here.
class RosterManager(models.Manager):

    def live(self):
        return self.model.objects.filter(is_active=True)

"""
    def create_roster(
        self,
        name,
        members,
        description='',
        city='',
        state='',
        status='',
    ):

        roster = self.model(
            name=name,
            description=description,
            city=city,
            state=state,
            status=status,
        )

        roster.save(using=self._db)
        return roster
"""


class Roster(models.Model):
    # roster name, chosen by whoever is creating it
    name = models.CharField(max_length=255, verbose_name='Group name')
    # points to the Player model table through the membership model
    members = models.ManyToManyField(Player, through='Membership')
    # moderator can write a blurb about
    description = models.TextField(blank=True)
    # group status, size of a tweet for future use
    status = models.CharField(max_length=140, blank=True)
    # city where most group members are located
    city = models.CharField(max_length=50, blank=True)
    # state that contains the city
    state = USStateField(blank=True)
    # zip code
    zipcode = USPostalCodeField(blank=True)
    # the date this roster was created
    date_created = models.DateField(auto_now_add=True)
    # when a moderator 'deletes' a group, it will be set inactive
    is_active = models.BooleanField(default=True)
    # allows users to see name, description, status, location of the group
    is_public = models.BooleanField(default=False)
    # slug for easy linking to group page
    slug = models.SlugField(max_length=255, blank=True, default='')

    #comments = models
    #games = models.ForeignKey(Game)

    objects = RosterManager()

    REQUIRED_FIELDS = ['name', ]

    class Meta:
        ordering = ["name",]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Roster, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("rosters:detail", (), {"slug": self.slug, "pk": self.id})


"""class MembershipManager(models.Manager):

    def live(self):
        return self.model.objects

    def create_membership(
        self,
        player,
        roster,
        is_moderator,
        invited_by,

    ):

        membership = self.model(
            player=player,
            roster=roster,
            is_moderator=is_moderator,
            invited_by=invited_by
        )

        membership.save(using=self._db)
        return membership
"""


class Membership(models.Model):
    """
    A 'player(user)' has access to a 'roster' through a 'membership' which
    keeps track of various information about that players relationship with
    each roster that they are a part of.
    """

    # key for the player whose membership this is
    player = models.ForeignKey(Player)
    # set to true if this player moderatres the associated roster
    is_moderator = models.BooleanField(default=False)
    # the roster to which this player belongs
    roster = models.ForeignKey(Roster)
    # the date/time at which the player joined (membership was created)
    date_joined = models.DateField(auto_now_add=True)
    # the username of the moderator who invited this player
    invited_by = models.CharField(max_length=255)
    # the number of total games this player has won in this roster
    games_won = models.SmallIntegerField(default=0)
    # the number of opponents killed over all games in this roster
    frags = models.SmallIntegerField(default=0)
    # the nubmer of times this player has died in this roster
    deaths = models.SmallIntegerField(default=0)
    # players can specify which aspects of their profile they'd
    # like to share, on a per-roster basis
    # not sure if this is the best way to model this...
    # in fact, it's very likely not...

    #objects = MembershipManager()

    REQUIRED_FIELDS = ['is_moderator', 'invited_by' ]

    def __unicode__(self):
        return str(self.id)
