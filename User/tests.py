from django.test import TestCase, Client
from django.contrib.auth.models import User
# from Register.models import Student
from django.urls import reverse, resolve
from User.views import login_view
# from django.contrib.auth.hashers import make_password

# Create your tests here.
class LogInViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        self.login_url = reverse('login')

    def test_templates_login(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'User/login.html')

    def test_url_login_view(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login_view)

    def test_conection_after_post(self):
        response = self.client.post(self.login_url, {"uname": "6410000212", "psw": "gobackn007"})
        self.assertIn(response.status_code, [200, 302])

    def test_HttpResponseRedirect(self):
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.post(self.login_url, {"uname": "6410000212", "psw": "gobackn007"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/registrar/')

    def test_user_is_none(self):
        response = self.client.post(self.login_url, {"uname": "6410000200", "psw": "007008ZA"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, text = 'Invalid credentials.')





