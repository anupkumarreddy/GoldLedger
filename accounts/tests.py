from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AuthenticationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="owner", password="testpass123")

    def test_protected_route_redirects_to_login(self):
        response = self.client.get(reverse("dashboard:index"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard:index')}")

    def test_home_redirects_authenticated_user_to_dashboard(self):
        self.client.login(username="owner", password="testpass123")
        response = self.client.get(reverse("accounts:home"))
        self.assertRedirects(response, reverse("dashboard:index"))
