"""
Models for advanced course.
"""
import math

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from model_utils.managers import InheritanceManager

from xmodule_django.models import CourseKeyField


class AdvancedCourseTypes(object):

    F2F = 'face_to_face'

    @classmethod
    def all(cls):
        return [cls.F2F]


class AdvancedCourseManager(InheritanceManager):

    def enabled(self):
        return self.filter(is_active=True)


class AdvancedCourse(models.Model):
    """
    Base model for advanced course
    """

    objects = AdvancedCourseManager()

    # must override in subclass
    course_type = None

    # the course that this advanced course is attached to
    course_id = CourseKeyField(max_length=255, db_index=True, verbose_name=_("course_id"))

    display_name = models.CharField(max_length=255, verbose_name=_("Display Name"))

    start_date = models.DateField(verbose_name=_("Start Date"))

    start_time = models.TimeField(verbose_name=_("Start Time"))

    end_time = models.TimeField(verbose_name=_("End Time"))

    capacity = models.IntegerField(default=0, verbose_name=_("Capacity"))

    # short description of advanced course. it must be text.
    description = models.CharField(max_length=1000, verbose_name=_("Description"))

    # long description of advanced course. it will allow html.
    content = models.TextField(blank=True, verbose_name=_("Other information"))

    # use this flag if end to advanced course manually.
    is_active = models.BooleanField(default=True, verbose_name=_("Enabled"))

    @classmethod
    def get_advanced_course(cls, advanced_course_id):
        return cls.objects.get_subclass(pk=advanced_course_id, is_active=True)

    @classmethod
    def get_advanced_courses_by_course_key(cls, course_key):
        return cls.objects.enabled().filter(course_id=course_key).select_subclasses()

    @property
    def tickets(self):
        return self.advancedcourseticket_set.all()

    def __unicode__(self):
        return u'{course_id} {display_name}'.format(course_id=self.course_id, display_name=self.display_name)


class AdvancedCourseTicket(models.Model):

    advanced_course = models.ForeignKey(AdvancedCourse, db_index=True, verbose_name=_("Face 2 Face Classroom"))

    display_name = models.CharField(max_length=255, verbose_name=_("Display Name"))

    price = models.IntegerField(default=0, verbose_name=_("Price of ticket"))

    sell_by_date = models.DateTimeField(verbose_name=_("Sell-by date"))

    description = models.CharField(max_length=255, verbose_name=_("Description"))

    display_order = models.IntegerField(default=99, verbose_name=_("Display Order"))

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Ticket")

    @property
    def tax(self):
        return int(math.floor(self.price * settings.PAYMENT_TAX / 100))

    @property
    def price_with_tax(self):
        return self.price + self.tax

    def is_end_of_sale(self):
        return self.sell_by_date < timezone.now()

    @classmethod
    def get_by_id(cls, ticket_id):
        return cls.objects.get(pk=ticket_id)

    @classmethod
    def find_by_advanced_course(cls, advanced_course):
        return cls.objects.filter(advanced_course=advanced_course).order_by('display_order')


class AdvancedF2FCourse(AdvancedCourse):
    """
    Model for face-to-face course
    """

    course_type = AdvancedCourseTypes.F2F

    place_name = models.CharField(max_length=100, blank=True, verbose_name=_("Meeting Place"))

    place_link = models.URLField(blank=True, verbose_name=_("Meeting Place Url"))

    place_address = models.CharField(max_length=255, blank=True, verbose_name=_("Address"))

    place_access = models.CharField(max_length=1000, blank=True, verbose_name=_("Access"))

    class Meta:
        verbose_name = _("Face 2 Face Classroom")
        verbose_name_plural = _("Face 2 Face Classroom")
