from django.db import models
from players.models import Player
from localflavor.us.models import USStateField
from django.template.defaultfilters import slugify
import datetime


# Create your models here.
class RosterManager(models.Manager):

    def live(self):
        return self.model.objects.filter(
            is_active=True
        ).select_related(
            'game'
        )

    def get_players(self):
        """
        returns a queryset of all members of the group and their
        associated player object
        """
        return self.model.objects.all().prefetch_related('members__player')
        #filter(id=id).prefetch_related('player')

    def get_mod_status(self, roster_id, player_id):
        return Membership.objects.filter(
            roster=roster_id
            ).filter(is_moderator=True, player=player_id)

    def get_mod_players(self, roster_id):
        return Membership.objects.filter(
            roster=roster_id
            ).filter(is_moderator=True)

    def get_all_members(self, roster_id):
        if roster_id is not None:
            return Membership.objects.filter(
                roster=roster_id
            ).prefetch_related('player')
        else:
            return Membership.objects.all()

    def get_active_members(self, roster_id):
        if roster_id is not None:
            return Membership.objects.filter(
                roster=roster_id,
                is_active=True
            ).prefetch_related('player')
        else:
            return Membership.objects.all()


class Roster(models.Model):
    # roster name, chosen by whoever is creating it
    name = models.CharField(max_length=255, verbose_name='Group name')
    # points to the Player model table through the membership model
    members = models.ManyToManyField(
        Player,
        through='Membership',
        through_fields=('roster', 'player')
    )

    # moderator can write a blurb about the group
    description = models.TextField(blank=True)
    # group status, size of a tweet for future use
    status = models.CharField(max_length=140, blank=True)
    # city where most group members are located
    city = models.CharField(max_length=50, blank=True)
    # state that contains the city
    state = USStateField(blank=True)
    # zip code
    zipcode = models.CharField(max_length=10, blank=True)
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
        ordering = ["name", ]

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Roster, self).save(*args, **kwargs)

    @models.permalink
    def get_absolute_url(self):
        return ("rosters:detail", (), {"slug": self.slug, "pk": self.id})


class MembershipManager(models.Manager):

    def live(self):
        return self.model.objects.all()

    def get_moderators(self):
        return self.model.objects.filter(is_moderator=True)

    def get_member(self, mem_id):
        return self.model.objects.filter(player=mem_id)


class Membership(models.Model):
    """
    A 'player(user)' has access to a 'roster' through a 'membership' which
    keeps track of various information about that players relationship with
    each roster that they are a part of.
    """

    # key for the player whose membership this is
    player = models.ForeignKey(Player, related_name="player")
    # set to true if this player moderatres the associated roster
    is_moderator = models.BooleanField(default=False)
    # the roster to which this player belongs
    roster = models.ForeignKey(Roster)
    # the date/time at which the player joined (membership was created)
    date_joined = models.DateField(auto_now_add=True)
    # the username of the moderator who invited this player
    invited_by = models.CharField(max_length=255, default='')
    #invited_by = models.CharField(max_length=255)
    # the number of total games this player has won in this roster
    games_won = models.SmallIntegerField(default=0)
    # the number of opponents killed over all games in this roster
    frags = models.SmallIntegerField(default=0)
    # the nubmer of times this player has died in this roster
    deaths = models.SmallIntegerField(default=0)
    # if a player wants to stay in the group, but doesn't want to
    # join in the next game, they can mark themselves as inactive.
    # When the moderator starts a game, inactive players will not
    # be added to the living_players list
    is_active = models.BooleanField(default=True)
    # players can specify which aspects of their profile they'd
    # like to share, on a per-roster basis
    # not sure if this is the best way to model this...
    # in fact, it's very likely not...

    objects = MembershipManager()

    REQUIRED_FIELDS = ['invited_by']

    def __unicode__(self):
        return str(self.id)


class GameManager(models.Manager):

    def live(self):
        return self.model.objects.filter(is_active=True)

    def get_for_group(self, id):
        return self.model.objects.filter(roster=id)


class Game(models.Model):
    """
    Each game essentially represents an instance of a roster.  Each
    game instance can have different rules, which are just enforced
    by the moderator or the players themselves (this is supposed to be
    for fun after all!).  The game keeps track of who is alive and who
    is dead, and is also responsible for shuffling the player list for
    random targets.  The list of targets is kept secret from everyone,
    including the moderator.  This is so that they can play the game
    without accusations of cheatery.  Each roster can only have 1
    active game at a time, so if there is a currently active game,
    a new one cannot be started until the old one finishes.

    """
    # the roster that this game is attached to
    roster = models.ForeignKey(Roster)
    # true if the game is currently in progress
    is_active = models.BooleanField(default=True)
    # stored as a comma separated list of usernames. List seems very
    # unlikely to go above 500 users in the extreme cases, so
    # I'd rather save the database lookup of foreign keys, and just
    # keep a list of the actual usernames.
    living_player_list = models.TextField(blank=True, default='')
    dead_player_list = models.TextField(blank=True, default='')
    # A place to list special rules for this instance of the game.
    # these rules would have to be enforced by the moderator, not
    # the game itself
    house_rules = models.TextField(blank=True)
    # if game finished naturally, mark true
    completed = models.BooleanField(default=False)
    # if game was cancelled, mark true
    cancelled = models.BooleanField(default=False)
    # date/time at which the game started
    start_time = models.DateTimeField(auto_now_add=True)
    # date/time at which the game ended, (regardless of complete or cancelled)
    end_time = models.DateTimeField(blank=True, null=True)

    # types the moderator can choose from when starting a game.  This
    # will affect how the game assigns targets
    MODE_CHOICES = (
        ('STD', 'Standard'),
        ('FFA', 'Free For All'),
        ('TDM', 'Team Deathmatch'),
        ('VIP', 'Protect the VIP'),
        ('ZOM', 'Zombie takeover'),
    )

    mode = models.CharField(
        max_length=3,
        choices=MODE_CHOICES,
        default='STD'
    )

    REQUIRED_FIELDS = ['mode', 'living_player_list']

    def __unicode__(self):
        return self.id

    class Meta:
        ordering = ["start_time", ]
