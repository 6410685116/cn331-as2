from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import Student, Subject
from .views import registrar, quota, quotalist
from django.contrib.messages import get_messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages import get_messages

# Create your tests here.
class TestArichive(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.registrar = reverse('registrar')
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        self.client.login(username="6410000212", password="gobackn007")
        self.student = Student.objects.create(Name ="terapat", Surname = "prirapon", Student_number = "6410000212", user= self.user)
    def test_url_registrar(self):
        self.assertEquals(resolve(self.registrar).func, registrar)
    def test_archive_templates(self):
        response = self.client.get(self.registrar)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/archive.html')
    def test_registrar_student(self):
        response = self.client.get(self.registrar)
        self.assertEquals(response.status_code, 200)
        self.assertIn('student', response.context)
        self.assertEqual(response.context['student'], self.student)

class TestQuota(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.quota = reverse('quota')
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        self.client.login(username="6410000212", password="gobackn007")
        self.student = Student.objects.create(Name ="terapat", Surname = "prirapon", Student_number = "6410000212", user= self.user)
        self.subject1 = Subject.objects.create(course = "DATA STRUCTURES I",
                                          id_course = "CN202",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 50,
                                          max_quota = 50,
                                          is_open = True,
                                          )
        self.subject2 = Subject.objects.create(course = "COMPUTER SERVER CONFIGURATIONT",
                                          id_course = "CN310",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 0,
                                          max_quota = 50,
                                          is_open = True,
                                          )
    def test_url_registrar(self):
        self.assertEquals(resolve(self.quota).func, quota)
    def test_quota_templates(self):
        response = self.client.get(self.quota)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/quota.html')
    def test_render_all_course(self):
        response = self.client.get(self.quota)
        self.assertEquals(response.status_code, 200)
        self.assertIn('all_course', response.context)
        for i in range(0, len([subject for subject in Subject.objects.exclude(students=self.student)])):
            self.assertEqual(
            response.context['all_course'][i],
            [subject for subject in Subject.objects.exclude(students=self.student)][i]
            )
    def test_reder_message(self):
        self.subject2.students.add(self.student)
        response = self.client.get(self.quota)
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "กดลงวิชาไม่ได้เนื่องจากเต็ม")
    def test_subject_is_open(self):
        self.subject1.is_open = False
        self.subject1.save()
        self.assertEqual(self.subject1.is_open, False)


class TestAddStudent(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.client = Client()
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        self.student = Student.objects.create(Name ="terapat", Surname = "prirapon", Student_number = "6410000212", user= self.user)
        self.subject1 = Subject.objects.create(course = "DATA STRUCTURES I",
                                          id_course = "CN202",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 50,
                                          max_quota = 50,
                                          is_open = True,
                                          )
        self.subject2 = Subject.objects.create(course = "COMPUTER SERVER CONFIGURATIONT",
                                          id_course = "CN310",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 0,
                                          max_quota = 50,
                                          is_open = True,
                                          )
    def test_add_student(self):
        self.client.login(username="6410000212", password="gobackn007")
        url = reverse('add_student', args=[int(self.subject1.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'Success')
        updated_course = Subject.objects.get(pk=self.subject1.id)
        self.assertEqual(updated_course.quota, 49)
    def test_add_student_quota_full_view(self):
        self.client.login(username="6410000212", password="gobackn007")
        url = reverse('add_student', args=[str(self.subject2.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['message'], 'โค้วต้าเต็ม')
        updated_course = Subject.objects.get(pk=self.subject2.id)
        self.assertEqual(updated_course.quota, 0)

class TestQuotaList(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.quotalist = reverse('quotalist')
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        self.client.login(username="6410000212", password="gobackn007")
        self.student = Student.objects.create(Name ="terapat", Surname = "prirapon", Student_number = "6410000212", user= self.user)
        self.subject1 = Subject.objects.create(course = "DATA STRUCTURES I",
                                          id_course = "CN202",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 50,
                                          max_quota = 50,
                                          is_open = True,
                                          )
        self.subject2 = Subject.objects.create(course = "COMPUTER SERVER CONFIGURATIONT",
                                          id_course = "CN310",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 0,
                                          max_quota = 50,
                                          is_open = True,
                                          )
    def test_url_listquota(self):
        self.assertEquals(resolve(self.quotalist).func, quotalist)
    def test_quotalist_templates(self):
        response = self.client.get(self.quotalist)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/listquota.html')
    def test_quotalist_view(self):
        response = self.client.get(self.quotalist)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['enrolled_courses'], [])
    def rest_quotalist_enrolled_courses(self):
        self.subject1.students.add(self.student)
        self.subject2.students.add(self.student)
        response = self.client.get(self.quotalist)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/listquota.html')
    def test_quotalist_view_with_enrolled_courses(self):
        self.subject1.students.add(self.student)
        self.subject2.students.add(self.student)
        response = self.client.get(self.quotalist)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/listquota.html')
        for i in range(0, len([subject for subject in Subject.objects.filter(students = self.student)])):
            self.assertEqual(
            response.context['enrolled_courses'][i],
            [subject for subject in Subject.objects.filter(students = self.student)][i]
            )

class TestDelete(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        self.client.login(username="6410000212", password="gobackn007")
        self.student = Student.objects.create(Name ="terapat", Surname = "prirapon", Student_number = "6410000212", user= self.user)
        self.subject1 = Subject.objects.create(course = "DATA STRUCTURES I",
                                          id_course = "CN202",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 0,
                                          max_quota = 50,
                                          is_open = True,
                                          )
        self.subject1.students.add(self.student)
    def test_delete_view(self):
        self.assertEqual(self.subject1.students.count(), 1)
        url = reverse('delete', args=[int(self.subject1.id)])
        response = self.client.get(url)
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(self.subject1.students.count(), 0)
        self.assertEqual(self.subject1.quota, 0)
    def test_delete_message(self):
        url = reverse('delete', args=[int(self.subject1.id)])
        response = self.client.get(url)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "เอาโค้วต้าออกเรียบร้อย")
    def test_redirect_delete(self):
        url = reverse('delete', args=[int(self.subject1.id)])
        response = self.client.get(url)
        self.assertEqual(response.url, "/listquota/")

class TestLogOutViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        self.client.login(username="6410000212", password="gobackn007")
        self.logout = reverse('logout')
    def test_logout_view(self):
        response = self.client.get(self.logout)
        if response.context is not None:
            user_in_context = response.context.get('user')
            if user_in_context:
                self.assertFalse(user_in_context.is_authenticated)
            else:
                self.assertIsInstance(response.context['user'], AnonymousUser)
    def test_message_logout_view(self):
        response = self.client.get(self.logout)
        messages = list(get_messages(response.wsgi_request))
        self.assertIn(response.status_code, [200, 302])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "I'm out")
    def test_redirect_login(self):
        response = self.client.get(self.logout)
        self.assertEqual(response.url, "/")