"""
Tests for the custom User model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from django.db import models

def create_user():
    """Create a new user."""
    email = "user@example.com"
    password = "password123"
    return get_user_model().objects.create_user(email, password)

class UserModelTests(TestCase):

    def test_successful_creating_user(self):
        """Check successful user creation with right email and password(hashed)."""
        email = "user@example.com"
        password = "password123"
        user = get_user_model().objects.create(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create(email, "password123")

            self.assertEqual(user.email, expected)

    def test_existing_user_email_normalized(self):
        """Test email is normalized for existing users updating their instances."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        user = create_user()
        for email, expected in sample_emails:
            user = user.email = email
            user.save()
            user.refresh_from_db()

            self.assertEqual(user.email,expected)

    def test_creating_user_without_email_raises_error(self):
        """Test raised ValueError when creating a user without email."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "password123")

    def test_deleting_user(self):
        """Test deleting user instances from the db."""
        user = create_user()
        user.delete()

        self.assertFalse(get_user_model().objects.exists())

    def test_creating_superuser_successful(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            "test@example.com",
            "password123"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
