from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Profile

class AccountsModelTest(TestCase):
    def test_profile_signal_creation(self):
        user = User.objects.create_user(username='testuser', password='password123')
        self.assertTrue(hasattr(user, 'profile'))
        self.assertIsInstance(user.profile, Profile)
        self.assertFalse(user.profile.dark_mode)
