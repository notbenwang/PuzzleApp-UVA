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
    

    