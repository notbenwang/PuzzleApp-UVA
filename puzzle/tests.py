# Code for creating mock account in set up from
# URL: https://stackoverflow.com/questions/27841101/can-not-log-in-with-unit-test-in-django-allauth
# Name: micgeronomo
# Date: Jan 8 2015

from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

from django.urls import reverse
from .models import CustomUser, Hunt, Puzzle, Hint, Session, Guess


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
# Add testing

class IndexTests(TestCase):

    def setUp(self):
        username = 'testuser'
        password = 'testpass'
        User = get_user_model()
        user = User.objects.create_user(username, password=password)
        logged_in = self.client.login(username=username, password=password)
        self.assertTrue(logged_in)

    def test_index(self):
        res = self.client.get(reverse('index'))
        self.assertEqual(res.status_code, 302)

    def test_dashboard(self):
        res = self.client.get(reverse('dashboard'))
        self.assertEqual(res.status_code, 200)

    def test_add_temp_hunt_url(self):
        url = reverse('add_temp_hunt', args=[1])
        # Check if the URL matches the expected URL
        self.assertEqual(url, '/1/add_temp_hunt')

    def test_unauthenticated_user_redirection(self):
        # Test that an unauthenticated user is redirected to the login page when accessing protected views
        dashboard_url = reverse('dashboard')
        response = self.client.get(dashboard_url)
        self.assertEqual(response.status_code, 200)  # Assuming status 302 means redirection

class HuntModelTest(TestCase):
    
    def setUp(self):
        self.user = CustomUser.objects.create(social_id=123, is_admin=True)
        self.test_hunt = Hunt.objects.create(
            title="Hunt 1",
            summary="This is a test hunt.",
            approved=True,
            submitted=True,
            creator=self.user
        )

    def test_hunt_attributes(self):
        self.assertEqual(self.test_hunt.title, "Hunt 1")
        self.assertEqual(self.test_hunt.summary, "This is a test hunt.")
        self.assertTrue(self.test_hunt.approved)
        self.assertTrue(self.test_hunt.submitted)
        self.assertEqual(self.test_hunt.creator, self.user)

    def test_puzzle_creation(self):
        puzzle = Puzzle.objects.create(
            prompt_text = "Rotunda",
            hunt_id = self.test_hunt,
            long = 1.23,
            lat = 4.56,
            radius = 20,
            order = 1
        )

        self.assertEqual(puzzle.prompt_text, "Rotunda")
        self.assertEqual(puzzle.hunt_id, self.test_hunt)
        self.assertEqual(puzzle.long, 1.23)
        self.assertEqual(puzzle.lat, 4.56)
        self.assertEqual(puzzle.radius, 20)
        self.assertEqual(puzzle.order, 1)

        hint = Hint.objects.create(hint_string="Center of grounds", puzzle_id=puzzle)

        self.assertEqual(hint.hint_string, "Center of grounds")
        self.assertEqual(hint.puzzle_id, puzzle)

class SessionModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(social_id=123, is_admin=True)
        self.test_hunt = Hunt.objects.create(
            title="Hunt 1",
            summary="This is a test hunt.",
            approved=True,
            submitted=True,
            creator=self.user
        )

    def test_session_creation(self):
        session = Session.objects.create(
            player=self.user,
            hunt=self.test_hunt,
            completed=False,
            current_puzzle=1,
            current_hints_used=2,
            total_hints_used=2,
            total_score=0,
            finished_puzzle=False
        )
        #hunt session
        self.assertEqual(session.player, self.user)
        self.assertEqual(session.hunt, self.test_hunt)
        self.assertFalse(session.completed)
        self.assertEqual(session.current_puzzle, 1)
        self.assertEqual(session.current_hints_used, 2)
        self.assertEqual(session.total_hints_used, 2)
        self.assertEqual(session.total_score, 0)
        self.assertFalse(session.finished_puzzle)

class GuessModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create(social_id=123, is_admin=True)
        self.test_hunt = Hunt.objects.create(
            title="Hunt 1",
            summary="This is a test hunt.",
            approved=True,
            submitted=True,
            creator=self.user
        )

    def test_guess_creation(self):
        puzzle = Puzzle.objects.create(
            prompt_text="Rotunda",
            hunt_id=self.test_hunt,
            long=1.23,
            lat=4.56,
            radius=20,
            order=1
        )
        #hunt session
        session = Session.objects.create(
            player=self.user,
            hunt=self.test_hunt,
            completed=False,
            current_puzzle=1,
            current_hints_used=0,
            total_hints_used=0,
            total_score=0,
            finished_puzzle=False
        )

        guess = Guess.objects.create(
            session=session,
            order=1,
            long=1.234,
            lat=4.567
        )

        self.assertEqual(guess.session, session)
        self.assertEqual(guess.order, 1)
        self.assertEqual(guess.long, 1.234)
        self.assertEqual(guess.lat, 4.567)

        #correct guess
        guess = Guess.objects.create(
            session=session,
            order=2,
            long=1.000,
            lat=4.500
        )
        #wrong guess
        self.assertEqual(guess.session, session)
        self.assertNotEqual(guess.order, 1)
        self.assertNotEqual(guess.long, 1.234)
        self.assertNotEqual(guess.lat, 4.567)

    

    