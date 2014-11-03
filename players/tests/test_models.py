from django.test import TestCase
from django.core.urlresolvers import reverse

from ..models import Player

# Create your tests here.

class PlayerTests(TestCase):

    def setUp(self):
        self.player = Player.objects.create(
            username='test',
            password='test',
            email='test@test.test'
        )

    def create_player(
        self,
        username,
        password='test_pw',
        email='test@test.test',
        first_name='test_fn',
        last_name='test_ln',
        home_address='test_ha',
        work_address='test_wa',
        home_zip='test_hz',
        work_zip='test_wz',
        phone_number='test-pn',
        is_active=True
    ):

        return Player.objects.create(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
            home_address=home_address,
            work_address=work_address,
            home_zip=home_zip,
            work_zip=work_zip,
            phone_number=phone_number,
            is_active=is_active
        )

    def test_model_creation_defaults(self):
        self.assertTrue(isinstance(self.player, Player))
        self.assertEqual(self.player.__unicode__(), self.player.username)
        self.assertEqual(self.player.first_name, self.player.get_short_name())
        self.assertFalse(self.player.is_admin)
        self.assertFalse(self.player.is_staff)
        self.assertTrue(self.player.is_active)
        self.assertFalse(self.player.is_phone_validated)
        self.assertFalse(self.player.is_email_verified)

        self.player.is_phone_validated = True
        self.assertTrue(self.player.phone_validated)

        self.player.is_email_verified = True
        self.assertTrue(self.player.email_verified)

        self.assertEqual(
            self.player.first_name + " " + self.player.last_name,
            self.player.get_full_name())
        self.assertEqual(self.player.username, self.player.get_slug_field())


    def test_model_url(self):
        self.assertEqual(self.player.get_absolute_url(),
            reverse('players:detail', kwargs={'slug': self.player.username})
        )

    def test_model_manager(self):
        active_user = self.create_player(username='test1')
        inactive_user = self.create_player(
            username='test2',
            is_active=False
        )
        self.assertIn(active_user, Player.objects.live())
        self.assertNotIn(inactive_user, Player.objects.live())
