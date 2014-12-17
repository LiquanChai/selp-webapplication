from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template import Template, Context
from django.test import TestCase
from django.utils.importlib import import_module
from django.utils.six import StringIO
from .models import Category, Quiz, Progress 
from .views import (QuizListView, CategoriesListView, QuizDetailView)

 

class TestCategory(TestCase):
    def setUp(self):
        self.c1 = Category.objects.new_category(category='hello world')

        self.c2 = Category.objects.new_category(category='Red')

    def test_categories(self):
        self.assertEqual(self.c1.category, 'hello-world')


class TestQuiz(TestCase):
    def setUp(self):
    	self.oldnum = len(Quiz.objects.all())
    	
        self.c1 = Category.objects.new_category(category='elderberries')

        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         category=self.c1)
        self.quiz2 = Quiz.objects.create(id=2,
                                         title='test quiz 2',
                                         description='d2',
                                         category=self.c1)
        self.quiz3 = Quiz.objects.create(id=3,
                                         title='test quiz 3',
                                         description='d3',
                                         category=self.c1)
        self.quiz4 = Quiz.objects.create(id=4,
                                         title='test quiz 4',
                                         description='d4',
                                         category=self.c1)

        self.newnum = len(Quiz.objects.all())

    def test_quiz_title(self):
        self.assertEqual(self.quiz1.title, 'test quiz 1')
        self.assertEqual(self.quiz2.title, 'test quiz 2')
        self.assertEqual(self.quiz3.title, 'test quiz 3')
        self.assertEqual(self.quiz4.title, 'test quiz 4')
        self.assertEqual(self.oldnum + 4, self.newnum)


class TestProgress(TestCase):
    def setUp(self):
        self.c1 = Category.objects.new_category(category='elderberries')
        self.c2 = Category.objects.new_category(category='elderberries')
        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         category=self.c1)

        self.quiz2 = Quiz.objects.create(id=2,
                                         title='test quiz 2',
                                         description='d2',
                                         category=self.c2)

        self.user = User.objects.create_user(username='hello',
                                             email='hello@hello.com',
                                             password='hello')

        self.p1 = Progress.objects.create(user=self.user)
        self.assertEqual(0, self.p1.total_score + self.p2.total_score)
        self.p1.score.add(self.quiz1)
        self.p1.score.add(self.quiz2)
        self.assertEqual(2, self.p1.total_score + self.p2.total_score)


