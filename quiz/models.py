from __future__ import unicode_literals
import re
import json
from django.core.urlresolvers import reverse
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
from django.utils.translation import ugettext as _
from django.utils.timezone import now
 

from model_utils.managers import InheritanceManager


class CategoryManager(models.Manager):
    """
    enable adding new category
    """
    def new_category(self, category):
        new_category = self.create(category=re.sub('\s+', '-', category)
                                   .lower())

        new_category.save()
        return new_category

 
class Category(models.Model):
    """
    category is a set of quizess, identified by verbose_name
    """
    category = models.CharField(
        verbose_name=_("Category"),
        max_length=250, blank=True,
        unique=True, null=True)

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.category



class Quiz(models.Model):
    """
    one quiz is one question, it is a multiple choice question with option A B C D.
    It can be repeated in different categories.
    arrtibute: title, description, score(passmark) reference to category
    """

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=60, blank=False,null=False)

    description = models.TextField(
        verbose_name=_("Description"),
        blank=False, null=False, help_text=_("a description of the quiz"))

    category = models.ForeignKey(
        Category,blank=False,null=False,
        verbose_name=_("Category"))
    A = models.BooleanField(default=False,help_text=_("Answer A is Correct"))
    B = models.BooleanField(default=False,help_text=_("Answer B is Correct"))
    C = models.BooleanField(default=False,help_text=_("Answer C is Correct"))
    D = models.BooleanField(default=False,help_text=_("Answer D is Correct"))

    pass_mark = models.SmallIntegerField(
        blank=True, default=1,
        help_text=_("score of this quiz"),
        validators=[MaxValueValidator(100)])
    def get_absolute_url(self):
        return reverse('quiz_category_list_matching', kwargs={'category_name': self.category.category})





class Progress(models.Model):
    """
    the process of a user answering question in a category.
    """
    user = models.OneToOneField("auth.User", verbose_name=_("User"))
    category = models.ForeignKey(Category)
    score = models.ManyToManyField('Quiz')
    total_score = models.IntegerField(default=0)
                                            
    class Meta:
        verbose_name = _("User Progress")
        verbose_name_plural = _("User progress records")

  