from django.db import models
from players.models import Player
from localflavor.us.models import USStateField
from django.template.defaultfilters import slugify


# Create your models here.
class RosterManager(models.Manager):

    def live(self):
        return self.model.objects.filter(
            is_active=True
        ).select_related(
            'game'
        ).order_by('start_time')

    def get_mod_status(self, roster_id, player_id):
        """
        Returns an entry if the player id provided
        has moderator privileges in the roster id
        provided.
        """
        return Membership.objects.filter(
            roster=roster_id
            ).filter(is_moderator=True, player=player_id)

    def get_mod_players(self, roster_id):
        """
        returns all players that have moderator status
        in a particular roster
        """
        return Membership.objects.filter(
            roster=roster_id
            ).filter(is_moderator=True)

    def get_all_members(self, roster_id):
        """
        return all member/player info for a
        particular roster
        """
        if roster_id is not None:
            return Membership.objects.filter(
                roster=roster_id
            ).prefetch_related('player')
        else:
            return Membership.objects.all()

    def get_approved_members(self, roster_id):
        """
        return a list of members who have been
        approved by a moderator
        """
        if roster_id is not None:
            return Membership.objects.filter(
                roster=roster_id,
                is_approved=True
            ).prefetch_related('player')

    def get_active_members(self, roster_id):
        """
        return all active players for this roster
        """
        if roster_id is not None:
            return Membership.objects.filter(
                roster=roster_id,
                is_active=True
            ).prefetch_related('player')
        else:
            return Membership.objects.all()

    def get_roster(self, roster_id):
        """
        return the roster based on its ID
        """
        if roster_id is not None:
            return self.model.objects.filter(id=roster_id)


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
    # %TODO add a logo static image field

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
        """
        Return all memberships that are marked as
        moderators.  There could be multiple for the
        same player ID, if that player moderates multiple
        groups
        """
        return self.model.objects.filter(is_moderator=True)

    def get_member(self, mem_id):
        """
        return a specific member based on their ID
        """
        return self.model.objects.filter(player=mem_id)

    def get_mod_count(self, mem_id):
        """
        count the number of membership a particular
        player has where they are the moderator, so that
        a hard limit can be imposed
        """
        return self.model.objects.filter(
            player=mem_id,
            is_moderator=True
        ).count()

    def get_member_groups(self, mem_id):
        """
        Based on a member id, return the roster
        information associated with that membership
        """
        return self.model.objects.filter(
            player=mem_id,
        ).select_related('roster').filter(
            is_active=True
        )

    def get_mem_in_group(self, mem_id, roster_id):
        """
        given a roster ID, and a membership ID,
        return the roster object
        """
        return self.model.objects.filter(
            player=mem_id,
            roster=roster_id
        )


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
    # the username of the moderator who approved this player
    approved_by = models.CharField(max_length=255, default='')
    # the number of total games this player has won in this roster
    games_won = models.SmallIntegerField(default=0)
    # the number of opponents killed over all games in this roster
    frags = models.SmallIntegerField(default=0)
    # the nubmer of times this player has died in this roster
    deaths = models.SmallIntegerField(default=0)
    # if a player leaves in the middle of a game, counts as a 'drop'
    games_dropped = models.SmallIntegerField(default=0)
    # total number of games a player has been involved in, regardless
    # of drop/win/lose
    total_games_played = models.SmallIntegerField(default=0)
    # if a player wants to stay in the group, but doesn't want to
    # join in the next game, they can mark themselves as inactive.
    # When the moderator starts a game, inactive players will not
    # be added to the living_players list
    is_active = models.BooleanField(default=True)
    # a player gets a membership as soon as they attempt to join
    # a group, but they can't view the goup or join a game until
    # a moderator approves their request to join by approving their
    # request.  This value is True by default so that when a roster
    # is first created, the mod doesn't have to approve himself.
    is_approved = models.BooleanField(default=True)
    # a list of which specific aspects of their profile
    # the player is sharing with the group
    # %TODO create sharedfields model
    #shared_info = models.ManyToManyField(SharedFields)

    objects = MembershipManager()

    REQUIRED_FIELDS = ['player', 'roster']

    class Meta:
        unique_together = ('player', 'roster')

    def __unicode__(self):
        return str(self.id)


class CommentManager(models.Manager):

    def live(self):
        """
        an inactive comment is essentially a
        deleted comment.  Moderator can deactivate
        a comment that was written on their group's
        page
        """
        return self.model.objects.filter(is_active=True)

    def get_roster(self, roster_id):
        """
        get all comments for a particular roster
        as well as the player info for the authors
        """
        return self.model.objects.filter(
            is_active=True,
            roster=roster_id,
        ).select_related('player')

    def get_player_comments(self, player_id):
        """
        get all comments for a particular player
        """
        return self.model.objects.filter(
            is_active=True,
            player=player_id
        )


class Comment(models.Model):
    """
    each group has a wall of comments that players can make at
    any time.  The moderator has the power to delete them (make them
    inactive so that they don't show up on the wall)
    """
    is_active = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=255, default='', blank=True)
    player = models.ForeignKey(Player)
    roster = models.ForeignKey(Roster)

    objects = CommentManager()

    REQUIRED_FIELDS = ['player', 'roster', 'text']

    class Meta:
        ordering = ["creation_time", ]

    def __unicode__(self):
        return str(self.id)


class GameManager(models.Manager):

    def live(self):
        return self.model.objects.filter(is_active=True)

    def get_for_group(self, id):
        """
        return all games associated with a
        particular roster
        """
        return self.model.objects.filter(roster=id)

    def get_recent_game(self, roster_id):
        """
        get all games for a roster, ordered by
        start time such that we get the most recent
        game as the first result
        """
        return self.model.objects.filter(
            roster=roster_id,
        ).order_by('-start_time')

    def get_action_list(self, id):
        """
        return all actions associated with a particular
        game ID
        """
        return self.model.objects.filter(
            id=id
            ).select_related('action_list')


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
    house_rules = models.TextField(
        blank=True,
        default="No rules defined",
        help_text="Describe any special rules that players of this game should ahere to"
    )
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
    # %TODO change this into a many to many relationship
    # with some kind of game_mode object, so that the choices
    # can be easily modified and more malleable
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

    REQUIRED_FIELDS = ['living_player_list']

    objects = GameManager()

    def __unicode__(self):
        return str(self.id)

    class Meta:
        ordering = ["start_time", ]


class ActionManager(models.Manager):

    def get_roster(self, roster_id):
        """
        get all actions associated with a
        particular roster
        """
        return self.model.objects.filter(
            roster=roster_id
        ).select_related('target', 'source')

    def get_game(self, game_id):
        """
        get all actions associated with a
        particular game instance
        """
        return self.model.objects.filter(
            game=game_id
        ).select_related('target', 'source')


class Action(models.Model):
    """
    The game state is made up of a series of actions.  The main action
    for almost any game mode is going to be "kill target" or "kill
    enemy player", however we also want to allow the user to give a
    description of the nature of the death. example:
        --<target> was garrotted while attempting to get in his car--
    These messages are provided by the users and the users are encouraged
    to get creative.  Future support might allow for inclusion of a death
    pic with the created action.
    """
    # an action is taken by a "source" player
    source = models.ForeignKey(Player, related_name="source")
    # an action is performed on a "target" player
    target = models.ForeignKey(Player, related_name="target")
    # an action belongs to a particular instance of "game"
    # a game has many actions
    game = models.ForeignKey(Game)
    # also keep track of which roster this action took place in
    # could theoretically find it through the game ID, but storing
    # one extra key will make queries much more simple with
    # acceptable extra space usage
    roster = models.ForeignKey(Roster)
    # the time at which this action took place
    creation_time = models.DateTimeField(auto_now_add=True)
    # the text description of the action. The first action
    # should be the announcement of the game starting.
    # In the future, all actions will result in player notification
    # if they opted for notifications.
    # max length is set to max length of a tweet for future potential
    # twitter integration
    flavor_text = models.CharField(
        max_length=140,
        blank=True,
        default=''
    )

    # link to a static image of the action
    # %TODO

    REQUIRED_FIELDS = ['source', 'target', 'game', 'flavor_text']

    objects = ActionManager()

    class Meta:
        ordering = ["creation_time", ]

    def __unicode__(self):
        return str(self.id)

    @models.permalink
    def get_absolute_url(self):
        return ("rosters:detail", (), {"slug": self.slug, "pk": self.roster_id})
