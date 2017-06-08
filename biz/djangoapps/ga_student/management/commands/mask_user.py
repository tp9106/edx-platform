"""
Management command to mask for users whose activation key has expired.
"""

import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from biz.djangoapps.util import mask_utils, datetime_utils
from openedx.core.djangoapps.course_global.models import CourseGlobalSetting
from student.models import Registration

log = logging.getLogger(__name__)


class Command(BaseCommand):
    """
    Mask for users whose activation key has expired 
    """
    help = """
    Usage: python manage.py lms --settings=aws mask_user [--debug]
    """

    def handle(self, *args, **options):
        log.info(u"Command mask_user started at {}.".format(datetime_utils.timezone_now()))

        min_datetime, max_datetime = datetime_utils.min_and_max_of_date(days_after=-settings.INTERVAL_DAYS_TO_MASK_UNACTIVATED_USER)
        mask_users = User.objects.filter(
            is_active=False,
            email__contains='@',
            registration__masked=False,
            registration__modified__isnull=False,
            registration__modified__lt=min_datetime,
        )
        global_courses_ids = set(CourseGlobalSetting.all_course_id())

        for user in mask_users:
            log.info(u"Masked user_id : {}.".format(user.id))
            mask_utils.optout_receiving_global_course_emails(user, global_courses_ids)
            mask_utils.mask_name(user)
            mask_utils.mask_email(user)
            mask_utils.disconnect_third_party_auth(user)
            reg = Registration.objects.get(user=user)
            reg.update_masked()

        log.info(u"Command mask_user finished at {}.".format(datetime_utils.timezone_now()))
