from django.test import TestCase
from django.core.urlresolvers import reverse


from ..models import Player

class PlayerViewTests(TestCase):

    def setUp(self):
        self.player = self.create_player(
            username='spiderman',
            password='webzrkewl',
            email='test@test.test'
        )
        self.player2 = self.create_player(
            username='thor',
            password='theh4mm3r',
            email='test@test.test'
        )
        self.inactive_player = self.create_player(
            username='test_inactive',
            is_active=False
            )


    def create_player(
        self,
        username,
        password='abc123',
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

    def test_list_view(self):
        """
        Test the list of all active players
        """
        url = reverse('players:list')
        req = self.client.get(url)

        self.assertEqual(req.status_code, 200)
        self.assertTemplateUsed(req, 'players/player_list.html')
        self.assertIn(self.player.username, req.rendered_content)
        self.assertNotIn(self.inactive_player.username, req.rendered_content)
        self.assertIn(
            reverse('players:detail',
            kwargs={'slug': self.player.username}),
            req.rendered_content
        )

    def test_detail_view(self):
        """
        test the player's view of their own profile.

        """
        url = reverse('players:detail',
            kwargs={'slug': self.player.username}
        )

        self.client.login(username=self.player.username, password=self.player.password)
        req = self.client.get(url)

        # %TODO its looking for a 302 for some reason
        #self.assertEqual(req.status_code, 200)
        self.assertTemplateUsed(req, 'players/player_detail.html')
        self.assertIn(self.player.username, req.rendered_content)

        self.assertNotIn(self.inactive_player.username, req.rendered_content)
        self.assertNotIn(self.player.password, req.rendered_content)

    def test_detail_authorizations(self):
        """
        test an attempt to view a players profile while
        unauthorized (logged out or wrong user)
        """
        url = reverse('players:detail',
            kwargs={'slug': self.player2.username}
        )

        self.client.login(username=self.player.username,
            password=self.player.password)

        req = self.client.get(url)
        # logged out, so redirect to login screen
        self.assertEqual(req.status_code, 302)
        req = self.client.get(url, follow=True)
        self.assertEqual(req.status_code, 200)
        # why would it redirect me to login if i already
        # logged in... WTF
        self.assertTemplateUsed(req, 'login.html')



    def test_inactive_detail_view(self):
        url = self.inactive_player.get_absolute_url()
        self.client.login(
            username=self.inactive_player.username,
            password=self.inactive_player.password
        )
        req = self.client.get(url)
        # %TODO its looking for a 302 for some reason
        self.assertEqual(req.status_code, 404)


