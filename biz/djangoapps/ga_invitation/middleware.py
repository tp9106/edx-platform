
from collections import namedtuple
import re

from django.conf import settings
from django.http import Http404
from django.utils.functional import SimpleLazyObject

from courseware.courses import get_course_with_access
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from biz.djangoapps.ga_contract.models import ContractDetail
from biz.djangoapps.ga_invitation.models import ContractRegister


SpocStatus = namedtuple('SpocStatus', 'is_spoc_course has_spoc_access')


def _get_spoc_status(user, course_id):

    def _get_spoc_contract_ids(course_key):
        return [
            contract_detail.contract.id
            for contract_detail in ContractDetail.find_enabled_spoc_by_course_key(
                course_key=course_key
            )
        ]

    def _has_staff_access(user, course_key):
        try:
            get_course_with_access(user, 'staff', course_key)
            return True
        except Http404:
            return False

    def _has_spoc_access(user, contract_ids):
        return ContractRegister.has_input_and_register_by_user_and_contract_ids(
            user=user,
            contract_ids=contract_ids
        )

    _spoc_contract_ids = _get_spoc_contract_ids(course_id)

    is_spoc_course = bool(_spoc_contract_ids)
    has_spoc_access = (
        is_spoc_course and
        (_has_staff_access(user, course_id) or _has_spoc_access(user, _spoc_contract_ids))
    )

    return SpocStatus(is_spoc_course, has_spoc_access)


class SpocStatusMiddleware(object):
    """
    Middleware to check for status of spoc access authentication.

    This middleware must be excecuted after the AuthenticationMiddleware
    """

    COURSE_URL_PATTERN = re.compile(r'^/courses/{}/'.format(settings.COURSE_ID_PATTERN))

    def process_request(self, request):

        matches = self.COURSE_URL_PATTERN.match(request.path)
        if matches:
            try:
                course_id = CourseKey.from_string(matches.group(1))
                spoc_status = SimpleLazyObject(lambda: _get_spoc_status(request.user, course_id))
            except InvalidKeyError:
                # this middleware does nothing if course_id is invalid
                spoc_status = SpocStatus(False, False)
        else:
            spoc_status = SpocStatus(False, False)

        request.spoc_status = spoc_status
