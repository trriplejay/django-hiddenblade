from django.test import TestCase
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from ..models import Player
from ..models import Roster


class modelTestMixin():
    def setUp(self):
        self.player1 = Player.objects.create(
            username='player1',
            password='mypass',
            email='player1@email.com')
        self.player2 = Player.objects.create(
            username='player2',
            password='mypass',
            email='player2@email.com')

        self.roster = Roster.objects.create(
            name='testName',
        )
        self.member1 = Membership.objects.create(
            roster=self.roster.id,
            player=self.player1
        )
        self.member2 = Membership.objects.create(
            roster=self.roster.id,
            player=self.player2
        )


class RosterTests(TestCase, modelTestMixin):

    def setUp(self):
        super(RosterTests, self).setUp()

    def create_roster(
        self,
        name,
        description='',
        status='',
        city='',
        state='',
        zipcode='',
        is_active=True,
        is_public=False,
    ):

        return Roster.objects.create(
            description=description,
            status=status,
            state=state,
            city=city,
            zipcode=zipcode,
            is_active=is_active,
            is_public=is_public,

        )


    def test_model_creation(self):

        self.assertEqual(self.roster.name, self.roster.__unicode__())
        self.assertIsInstance(self.roster, Roster)
        self.assertEqual(self.roster.slug, slugify(self.roster.name))
        self.assertEqual(
            self.roster.get_absolute_url(),
            reverse(
                "rosters:detail",
                kwargs={
                    'slug': self.roster.slug,
                    'pk': self.roster.id
                }
            )
        )
        self.assertTrue(self.roster.is_active)
        self.assertFalse(self.roster.is_public)
        self.assertEqual(self.roster.description, '')
        self.assertEqual(self.roster.status, '')
        self.assertEqual(self.roster.state, '')
        self.assertEqual(self.roster.zipcode, '')
        self.assertEqual(self.roster.city, '')

    def test_model_manager(self):

        inactive_roster = self.create_roster(name="inactive", is_active=False)
        self.assertNotIn(self.roster, Roster.objects.get_roster(inactive_roster.id))
        self.assertIn(self.roster, Roster.objects.get_roster(self.roster.id))
        self.assertNotIn(inactive_roster, repr(Roster.objects.live()))

class MembershipTests(TestCase, modelTestMixin):

    def setUp(self):
        pass
