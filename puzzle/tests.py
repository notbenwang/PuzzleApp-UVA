from django.test import TestCase
from .models import Hunt
from .views import add_hunt, add_puzzle  # Import your view functions as needed

class HuntModelTests(TestCase):
    def test_add_hunt_and_go_back(self):
        # Ensure adding a hunt and then going back does not add a hunt to the database.
        initial_hunt_count = Hunt.objects.count()
        response = self.client.post('/add_hunt/', {'hunt_name': 'Test Hunt'})
        self.assertEqual(response.status_code, 200)  # Assuming a successful hunt addition redirects to the same page
        self.assertEqual(Hunt.objects.count(), initial_hunt_count)

    def test_add_hunt_and_submit(self):
        # Ensure adding a hunt and then submitting adds a hunt to the database.
        initial_hunt_count = Hunt.objects.count()
        response = self.client.post('/add_hunt/', {'hunt_name': 'Test Hunt', 'submit': 'Submit'})
        self.assertEqual(response.status_code, 302)  # Assuming a successful hunt addition redirects to some other URL
        self.assertEqual(Hunt.objects.count(), initial_hunt_count + 1)

    def test_add_hunt_with_puzzles_and_submit(self):
        # Ensure adding a hunt with puzzles and then submitting adds a hunt and its puzzles to the database.
        initial_hunt_count = Hunt.objects.count()
        initial_puzzle_count = Puzzle.objects.count()  # Assuming you have a 'Puzzle' model
        response = self.client.post('/add_hunt/', {'hunt_name': 'Test Hunt', 'add_puzzle': 'Add Puzzle', 'submit': 'Submit'})
        self.assertEqual(response.status_code, 302)  # Assuming a successful hunt addition redirects to some other URL
        self.assertEqual(Hunt.objects.count(), initial_hunt_count + 1)
        self.assertEqual(Puzzle.objects.count(), initial_puzzle_count + 1)  # Update this based on your actual model

    def test_add_hunt_with_puzzles_and_go_back(self):
        # Ensure adding a hunt with puzzles and then going back does not add hunts or puzzles to the database.
        initial_hunt_count = Hunt.objects.count()
        initial_puzzle_count = Puzzle.objects.count()  # Assuming you have a 'Puzzle' model
        response = self.client.post('/add_hunt/', {'hunt_name': 'Test Hunt', 'add_puzzle': 'Add Puzzle'})
        self.assertEqual(response.status_code, 200)  # Assuming going back redirects to the same page
        self.assertEqual(Hunt.objects.count(), initial_hunt_count)
        self.assertEqual(Puzzle.objects.count(), initial_puzzle_count)
