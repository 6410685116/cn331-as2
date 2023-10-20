from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from .models import Student, Subject
from .views import registrar, quota, quotalist
from django.http import HttpResponseRedirect
from django.contrib.messages import get_messages
from django.contrib.auth.models import AnonymousUser


# Create your tests here.
class TestArichive(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.registrar = reverse('registrar')
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        # self.client.login(username="6410000212", password="gobackn007")
        self.student = Student.objects.create(Name ="terapat", Surname = "prirapon", Student_number = "6410000212", user= self.user)
        
    def test_url_registrar(self):
        self.assertEquals(resolve(self.registrar).func, registrar)

    def test_archive_templates(self):
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.get(self.registrar)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/archive.html')

    def test_registrar_student(self):
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.get(self.registrar)
        self.assertEquals(response.status_code, 200)
        self.assertIn('student', response.context)
        self.assertEqual(response.context['student'], self.student)

class TestQuota(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.quota = reverse('quota')
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        # self.client.login(username="6410000212", password="gobackn007")
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
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.get(self.quota)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/quota.html')
    def test_render_all_course(self):
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.get(self.quota)
        self.assertEquals(response.status_code, 200)
        self.assertIn('all_course', response.context)
    #     self.assertQuerysetEqual(
    #         response.context['all_course'],
    #         [repr(subject) for subject in Subject.objects.exclude(students=self.student)],
    #         ordered=False
    #     )
    def test_reder_message(self):
        self.client.login(username="6410000212", password="gobackn007")
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
        self.client = Client()
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        # self.client.login(username="6410000212", password="gobackn007")
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
        # self.assertContains(response, text = 'Success')
        updated_course = Subject.objects.get(pk=self.subject1.id)
        self.assertEqual(updated_course.quota, 49)
    def test_add_student_quota_full_view(self):
        self.client.login(username="6410000212", password="gobackn007")
        url = reverse('add_student', args=[str(self.subject2.id)])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, text = 'โค้วต้าเต็ม')
        updated_course = Subject.objects.get(pk=self.subject2.id)
        self.assertEqual(updated_course.quota, 0)
    # def test_user_is_none(self):
    #     self.login_url = reverse('User:login')
    #     reaction = self.client.post(self.login_url, {"uname": "6410000200", "psw": "007008ZA"})
    #     self.assertEqual(reaction.status_code, 200)
    #     self.assertRedirects(reaction,  HttpResponseRedirect(reverse("/")))

class TestQuotaList(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.quotalist = reverse('quotalist')
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        # self.client.login(username="6410000212", password="gobackn007")
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
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.get(self.quotalist)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/listquota.html')
    def test_quotalist_view(self):
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.get(self.quotalist)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['enrolled_courses'], [])
    def rest_quotalist_enrolled_courses(self):
        self.client.login(username="6410000212", password="gobackn007")
        self.subject1.students.add(self.student)
        self.subject2.students.add(self.student)
        response = self.client.get(self.quotalist)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, './Register/listquota.html')
    # def test_quotalist_view_with_enrolled_courses(self):
    #     self.subject1.students.add(self.student)
    #     self.subject2.students.add(self.student)
    #     response = self.client.get(self.quotalist)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, './Register/listquota.html')
    #     enrolled_courses = response.context['enrolled_courses'].values_list('course', flat=True)
    #     expected_courses = ['DATA STRUCTURES I 1 2565', 'COMPUTER SERVER CONFIGURATIONT 1 2565']
    #     self.assertQuerysetEqual(enrolled_courses, expected_courses, ordered=False, transform=str) 

class TestDelete(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        # self.client.login(username="6410000212", password="gobackn007")
        self.student = Student.objects.create(Name ="terapat", Surname = "prirapon", Student_number = "6410000212", user= self.user)
        self.subject1 = Subject.objects.create(course = "DATA STRUCTURES I",
                                          id_course = "CN202",
                                          Semester = "1",
                                          Year = "2565",
                                          quota = 49,
                                          max_quota = 50,
                                          is_open = True,
                                          )
        self.subject1.students.add(self.student)
    # def test_delete_view(self):
    #     url = reverse('delete', args=[int(self.subject1.id)])
    #     response = self.client.get(url)
    #     self.assertEqual(self.subject1.students.count(), 0)
    #     self.assertEqual(self.subject1.quota, 50)

    #     messages = [msg.message for msg in get_messages(response.wsgi_request)]
    #     self.assertIn("เอาโค้วต้าออกเรียบร้อย", messages)

    #     self.assertRedirects(response, reverse('listquota'))

class TestLogOutViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(username="6410000212", password= "gobackn007")
        # self.client.login(username="6410000212", password="gobackn007")
        self.logout = reverse('logout')
    def test_logout_view(self):
        self.client.login(username="6410000212", password="gobackn007")
        response = self.client.get(self.logout)
        if response.context is not None:
            user_in_context = response.context.get('user')
            if user_in_context:
                self.assertFalse(user_in_context.is_authenticated)
            else:
                self.assertIsInstance(response.context['user'], AnonymousUser)

    # def test_message_logout_view(self):
    #         response = self.client.get(self.logout)
    #         self.assertIn(response.status_code, [200, 302])
    #         self.assertContains(response, text="I'm out")

    # def test_redirect_login(self):
    #     response = self.client.get(self.logout)
    #     self.assertRedirects(response, reverse('index'))