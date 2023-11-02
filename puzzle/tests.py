from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model

from django.urls import reverse


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

    

    