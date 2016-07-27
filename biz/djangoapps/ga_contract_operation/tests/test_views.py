"""
Test for contract_operation feature
"""
from datetime import datetime, timedelta
import ddt
import hashlib
import json
from mock import patch
import pytz

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.test.utils import override_settings

from biz.djangoapps.ga_contract_operation.models import ContractTaskHistory
from biz.djangoapps.ga_contract_operation.tests.factories import ContractTaskHistoryFactory
from biz.djangoapps.ga_invitation.models import ContractRegister, INPUT_INVITATION_CODE, REGISTER_INVITATION_CODE, UNREGISTER_INVITATION_CODE
from biz.djangoapps.ga_invitation.tests.factories import ContractRegisterFactory
from biz.djangoapps.ga_invitation.tests.test_views import BizContractTestBase
from openedx.core.djangoapps.ga_task.models import Task
from openedx.core.djangoapps.ga_task.tests.factories import TaskFactory
from openedx.core.lib.ga_datetime_utils import to_timezone
from student.models import CourseEnrollment
from student.tests.factories import UserFactory


@ddt.ddt
class ContractOperationViewTest(BizContractTestBase):

    # ------------------------------------------------------------
    # Register students
    # ------------------------------------------------------------
    def test_register_students(self):
        self.setup_user()
        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.assert_request_status_code(200, reverse('biz:contract_operation:register_students'))

    # ------------------------------------------------------------
    # Register students ajax
    # ------------------------------------------------------------
    def _url_register_students_ajax(self):
        return reverse('biz:contract_operation:register_students_ajax')

    def test_register_contract_unmatch(self):
        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_1,tester2"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'contract_id': self.contract_mooc.id, 'students_list': csv_content})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Current contract is changed. Please reload this page.')

    def test_register_no_param(self):
        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_1,tester2"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Unauthorized access.')

    def test_register_no_param_students_list(self):
        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_1,tester2"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'contract_id': self.contract_mooc.id})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Unauthorized access.')

    def test_register_no_param_contract_id(self):
        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_1,tester2"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'students_list': csv_content})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Unauthorized access.')

    def test_register_no_student(self):
        self.setup_user()
        csv_content = ""

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'contract_id': self.contract.id, 'students_list': csv_content})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Could not find student list.')

    def test_register_student_not_allowed_method(self):
        response = self.client.get(self._url_register_students_ajax())
        self.assertEqual(405, response.status_code)

    def test_register_student_submit_successful(self):
        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_1,tester2"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'contract_id': self.contract.id, 'students_list': csv_content})

        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("Began the processing of Student Register.Execution status, please check from the task history.", data['info'])

        # get latest task and assert
        task = Task.objects.all().order_by('-id')[0]
        self.assertEqual('student_register', task.task_type)

        task_input = json.loads(task.task_input)
        self.assertEqual(self.contract.id, task_input['contract_id'])
        history = ContractTaskHistory.objects.get(pk=task_input['history_id'])
        self.assertEqual(history.task_id, task.task_id)
        self.assertItemsEqual(csv_content.splitlines(), [target.student for target in history.studentregistertasktarget_set.all()])

    def test_register_student_submit_duplicated(self):
        TaskFactory.create(task_type='student_register', task_key=hashlib.md5(str(self.contract.id)).hexdigest())
        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_1,tester2"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'contract_id': self.contract.id, 'students_list': csv_content})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("Processing of Student Register is running.Execution status, please check from the task history.", data['error'])
        # assert not to be created new Task instance.
        self.assertEqual(1, Task.objects.count())

    @override_settings(BIZ_MAX_REGISTER_NUMBER=2)
    def test_register_students_over_max_number(self):

        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_2,tester2\n" \
                      "test_student3@example.com,test_student_3,tester3"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'contract_id': self.contract.id, 'students_list': csv_content})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("It has exceeded the number(2) of cases that can be a time of registration.", data['error'])

        self.assertFalse(User.objects.filter(username='test_student_1', email='test_student1@example.com').exists())
        self.assertFalse(User.objects.filter(username='test_student_2', email='test_student2@example.com').exists())
        self.assertFalse(User.objects.filter(username='test_student_3', email='test_student3@example.com').exists())

        self.assertFalse(ContractRegister.objects.filter(user__email='test_student1@example.com', contract=self.contract).exists())
        self.assertFalse(ContractRegister.objects.filter(user__email='test_student2@example.com', contract=self.contract).exists())
        self.assertFalse(ContractRegister.objects.filter(user__email='test_student3@example.com', contract=self.contract).exists())

    @override_settings(BIZ_MAX_CHAR_LENGTH_REGISTER_LINE=47)
    def test_register_students_over_max_char_length(self):

        self.setup_user()
        csv_content = "test_student1@example.com,test_student_1,tester1\n" \
                      "test_student2@example.com,test_student_2,tester2\n" \
                      "test_student3@example.com,test_student_3,tester3"

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_register_students_ajax(), {'contract_id': self.contract.id, 'students_list': csv_content})

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("The number of lines per line has exceeded the 47 lines.", data['error'])

        self.assertFalse(User.objects.filter(username='test_student_1', email='test_student1@example.com').exists())
        self.assertFalse(User.objects.filter(username='test_student_2', email='test_student2@example.com').exists())
        self.assertFalse(User.objects.filter(username='test_student_3', email='test_student3@example.com').exists())

        self.assertFalse(ContractRegister.objects.filter(user__email='test_student1@example.com', contract=self.contract).exists())
        self.assertFalse(ContractRegister.objects.filter(user__email='test_student2@example.com', contract=self.contract).exists())
        self.assertFalse(ContractRegister.objects.filter(user__email='test_student3@example.com', contract=self.contract).exists())

    # ------------------------------------------------------------
    # Students
    # ------------------------------------------------------------
    def test_students(self):
        self.setup_user()
        # view student management
        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.assert_request_status_code(200, reverse('biz:contract_operation:students'))
        self.assertNotIn(str(self.user.email), response.content)

        # register
        self.create_contract_register(self.user, self.contract)

        # view student management
        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.assert_request_status_code(200, reverse('biz:contract_operation:students'))
        self.assertIn(str(self.user.email), response.content)

    # ------------------------------------------------------------
    # Unregister students
    # ------------------------------------------------------------
    def _url_unregister_students_ajax(self):
        return reverse('biz:contract_operation:unregister_students_ajax')

    def test_unregister_get(self):
        self.setup_user()
        register = ContractRegisterFactory.create(user=self.user, contract=self.contract, status=INPUT_INVITATION_CODE)

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.get(self._url_unregister_students_ajax(), {'contract_id': self.contract.id, 'target_list': [register.id]})

        self.assertEqual(response.status_code, 405)

    def test_unregister_no_param(self):
        self.setup_user()

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_unregister_students_ajax(), {})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Unauthorized access.')

    def test_unregister_contract_unmatch(self):
        self.setup_user()
        register = ContractRegisterFactory.create(user=self.user, contract=self.contract, status=INPUT_INVITATION_CODE)

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract_mooc.id, 'target_list': [register.id]})

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Current contract is changed. Please reload this page.')

    def test_unregister_validate_not_found_register(self):
        self.setup_user()
        register_mooc = ContractRegisterFactory.create(user=self.user, contract=self.contract_mooc, status=INPUT_INVITATION_CODE)

        with self.skip_check_course_selection(current_contract=self.contract), patch('biz.djangoapps.ga_contract_operation.views.log.warning') as warning_log:
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract.id, 'target_list': [register_mooc.id]})
            warning_log.assert_called_with('Not found register in contract_id({}) contract_register_id({}), user_id({})'.format(self.contract.id, register_mooc.id, self.user.id))

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Unauthorized access.')

    def test_unregister_validate_warning(self):
        self.setup_user()
        register = ContractRegisterFactory.create(user=self.user, contract=self.contract, status=UNREGISTER_INVITATION_CODE)

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract.id, 'target_list': [register.id]})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['info'], 'Succeed to unregister 0 users.Already unregisterd 1 users.')

    def test_unregister_spoc(self):
        self.setup_user()
        register = ContractRegisterFactory.create(user=self.user, contract=self.contract, status=REGISTER_INVITATION_CODE)
        CourseEnrollment.enroll(self.user, self.course_spoc1.id)
        CourseEnrollment.enroll(self.user, self.course_spoc2.id)

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract.id, 'target_list': [register.id]})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['info'], 'Succeed to unregister 1 users.')

        self.assertEquals(ContractRegister.objects.get(user=self.user, contract=self.contract).status, UNREGISTER_INVITATION_CODE)
        self.assertFalse(CourseEnrollment.is_enrolled(self.user, self.course_spoc1.id))
        self.assertFalse(CourseEnrollment.is_enrolled(self.user, self.course_spoc2.id))

    def test_unregister_mooc(self):
        self.setup_user()
        register_mooc = ContractRegisterFactory.create(user=self.user, contract=self.contract_mooc, status=REGISTER_INVITATION_CODE)
        CourseEnrollment.enroll(self.user, self.course_mooc1.id)

        with self.skip_check_course_selection(current_contract=self.contract_mooc):
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract_mooc.id, 'target_list': [register_mooc.id]})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['info'], 'Succeed to unregister 1 users.')

        self.assertEquals(ContractRegister.objects.get(user=self.user, contract=self.contract_mooc).status, UNREGISTER_INVITATION_CODE)
        self.assertTrue(CourseEnrollment.is_enrolled(self.user, self.course_mooc1.id))

    def test_unregister_spoc_staff(self):
        self.setup_user()
        register = ContractRegisterFactory.create(user=self.user, contract=self.contract, status=REGISTER_INVITATION_CODE)
        CourseEnrollment.enroll(self.user, self.course_spoc1.id)
        CourseEnrollment.enroll(self.user, self.course_spoc2.id)

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract.id, 'target_list': [register.id]})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['info'], 'Succeed to unregister 1 users.')

        self.assertEquals(ContractRegister.objects.get(user=self.user, contract=self.contract).status, UNREGISTER_INVITATION_CODE)
        self.assertTrue(CourseEnrollment.is_enrolled(self.user, self.course_spoc1.id))
        self.assertTrue(CourseEnrollment.is_enrolled(self.user, self.course_spoc2.id))

    def test_unregister_spoc_staff(self):
        self.setup_user()
        # to be staff
        self.user.is_staff = True
        self.user.save()
        register = ContractRegisterFactory.create(user=self.user, contract=self.contract, status=REGISTER_INVITATION_CODE)
        CourseEnrollment.enroll(self.user, self.course_spoc1.id)
        CourseEnrollment.enroll(self.user, self.course_spoc2.id)

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract.id, 'target_list': [register.id]})

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEquals(data['info'], 'Succeed to unregister 1 users.')

        self.assertEquals(ContractRegister.objects.get(user=self.user, contract=self.contract).status, UNREGISTER_INVITATION_CODE)
        self.assertTrue(CourseEnrollment.is_enrolled(self.user, self.course_spoc1.id))
        self.assertTrue(CourseEnrollment.is_enrolled(self.user, self.course_spoc2.id))

    def test_unregister_db_error(self):
        self.setup_user()
        register = ContractRegisterFactory.create(user=self.user, contract=self.contract, status=REGISTER_INVITATION_CODE)
        CourseEnrollment.enroll(self.user, self.course_spoc1.id)
        CourseEnrollment.enroll(self.user, self.course_spoc2.id)

        with self.skip_check_course_selection(current_contract=self.contract), \
            patch('biz.djangoapps.ga_contract_operation.views.log.exception') as exception_log, \
            patch('biz.djangoapps.ga_contract_operation.views.ContractRegister.save', side_effect=IntegrityError()):
            response = self.client.post(self._url_unregister_students_ajax(), {'contract_id': self.contract.id, 'target_list': [register.id]})
            exception_log.assert_called_with('Can not unregister. contract_id({}), unregister_list({})'.format(self.contract.id, [register.id]))

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Failed to batch unregister. Please operation again after a time delay.')

        self.assertEquals(ContractRegister.objects.get(user=self.user, contract=self.contract).status, REGISTER_INVITATION_CODE)
        self.assertTrue(CourseEnrollment.is_enrolled(self.user, self.course_spoc1.id))
        self.assertTrue(CourseEnrollment.is_enrolled(self.user, self.course_spoc2.id))

    # ------------------------------------------------------------
    # Personalinfo Mask
    # ------------------------------------------------------------
    @property
    def _url_personalinfo_mask(self):
        return reverse('biz:contract_operation:personalinfo_mask')

    def test_personalinfo_mask_not_allowed_method(self):
        response = self.client.get(self._url_personalinfo_mask)
        self.assertEqual(405, response.status_code)

    def test_personalinfo_mask_submit_successful(self):
        """
        Tests success to submit. Processing of task is tested in test_tasks.py
        """
        registers = [
            self.create_contract_register(UserFactory.create(), self.contract),
            self.create_contract_register(UserFactory.create(), self.contract),
        ]
        params = {'target_list': [register.id for register in registers], 'contract_id': self.contract.id}

        self.setup_user()

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_personalinfo_mask, params)

        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("Began the processing of Personal Information Mask.Execution status, please check from the task history.", data['info'])

        # get latest task and assert
        task = Task.objects.all().order_by('-id')[0]
        self.assertEqual('personalinfo_mask', task.task_type)

        task_input = json.loads(task.task_input)
        self.assertEqual(self.contract.id, task_input['contract_id'])
        history = ContractTaskHistory.objects.get(pk=task_input['history_id'])
        self.assertEqual(history.task_id, task.task_id)
        self.assertItemsEqual(registers, [target.register for target in history.contracttasktarget_set.all()])

    def test_personalinfo_mask_submit_duplicated(self):
        registers = [
            self.create_contract_register(UserFactory.create(), self.contract),
            self.create_contract_register(UserFactory.create(), self.contract),
        ]
        params = {'target_list': [register.id for register in registers], 'contract_id': self.contract.id}
        TaskFactory.create(task_type='personalinfo_mask', task_key=hashlib.md5(str(self.contract.id)).hexdigest())

        self.setup_user()

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_personalinfo_mask, params)

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("Processing of Personal Information Mask is running.Execution status, please check from the task history.", data['error'])
        # assert not to be created new Task instance.
        self.assertEqual(1, Task.objects.count())

    @ddt.data('target_list', 'contract_id')
    def test_personalinfo_mask_missing_params(self, param):
        params = {'target_list': [1, 2], 'contract_id': 1, }
        del params[param]

        self.setup_user()
        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_personalinfo_mask, params)

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("Unauthorized access.", data['error'])

    def test_personalinfo_mask_contract_unmatch(self):
        params = {'target_list': [1, 2], 'contract_id': self.contract_mooc.id, }

        self.setup_user()
        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_personalinfo_mask, params)

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEqual("Current contract is changed. Please reload this page.", data['error'])

    def test_personalinfo_mask_register_unmatch(self):
        registers = [
            self.create_contract_register(UserFactory.create(), self.contract),
            self.create_contract_register(UserFactory.create(), self.contract_mooc),
        ]
        params = {'target_list': [register.id for register in registers], 'contract_id': self.contract.id, }

        self.setup_user()

        with self.skip_check_course_selection(current_contract=self.contract), patch('biz.djangoapps.ga_contract_operation.views.log.warning') as warning_log:
            response = self.client.post(self._url_personalinfo_mask, params)

        warning_log.assert_called_with(
            "Not found register in contract_id({}) contract_register_id({}), user_id({})".format(
                self.contract.id, registers[1].id, registers[1].user_id
            )
        )

        self.assertEqual(400, response.status_code)
        data = json.loads(response.content)
        self.assertEquals(data['error'], 'Unauthorized access.')

    # ------------------------------------------------------------
    # Task History
    # ------------------------------------------------------------
    @property
    def _url_task_history_ajax(self):
        return reverse('biz:contract_operation:task_history')

    def _create_task(self, task_type, task_key, task_id, task_state, total=0, attempted=0, succeeded=0, skipped=0, failed=0):
        task_output = {
            'total': total,
            'attempted': attempted,
            'succeeded': succeeded,
            'skipped': skipped,
            'failed': failed,
        }
        return TaskFactory.create(
            task_type=task_type, task_key=task_key, task_id=task_id, task_state=task_state, task_output=json.dumps(task_output)
        )

    def _assert_task_history(self, history, recid, task_type, state, requester, created, total=0, succeeded=0, skipped=0, failed=0):
        self.assertEqual(history['recid'], recid)
        self.assertEqual(history['task_type'], task_type)
        self.assertEqual(history['task_state'], state)
        self.assertEqual(history['task_result'], "Total: {}, Success: {}, Skipped: {}, Failed: {}".format(total, succeeded, skipped, failed))
        self.assertEqual(history['requester'], requester)
        self.assertEqual(history['created'], to_timezone(created).strftime('%Y/%m/%d %H:%M:%S'))

    def test_task_history(self):
        self.setup_user()
        tasks = [
            self._create_task('personalinfo_mask', 'key1', 'task_id1', 'SUCCESS', 1, 1, 1, 0, 0),
            self._create_task('personalinfo_mask', 'key2', 'task_id2', 'FAILURE', 1, 1, 0, 1, 0),
            self._create_task('personalinfo_mask', 'key3', 'task_id3', 'QUEUING', 1, 1, 0, 0, 1),
            self._create_task('dummy_task', 'key4', 'task_id4', 'PROGRESS'),
            self._create_task('dummy_task', 'key5', 'tesk_id5', 'DUMMY'),
        ]
        # Create histories for target contract
        histories = [ContractTaskHistoryFactory.create(contract=self.contract, requester=self.user) for i in range(6)]
        _now = datetime.now(pytz.UTC)
        for i, history in enumerate(histories):
            if i < len(tasks):
                history.task_id = tasks[i].task_id
                history.created = _now + timedelta(seconds=i)
                history.save()
        # Create histories for other contract
        ContractTaskHistoryFactory.create(contract=self.contract_mooc)

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_task_history_ajax, {})

        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual('success', data['status'])
        self.assertEqual(5, data['total'])
        records = data['records']
        self._assert_task_history(records[0], 1, 'Unknown', 'Unknown', self.user.username, histories[4].created)
        self._assert_task_history(records[1], 2, 'Unknown', 'In Progress', self.user.username, histories[3].created)
        self._assert_task_history(records[2], 3, 'Personal Information Mask', 'Waiting', self.user.username, histories[2].created, 1, 0, 0, 1)
        self._assert_task_history(records[3], 4, 'Personal Information Mask', 'Complete', self.user.username, histories[1].created, 1, 0, 1, 0)
        self._assert_task_history(records[4], 5, 'Personal Information Mask', 'Complete', self.user.username, histories[0].created, 1, 1, 0, 0)

    def test_task_history_zero(self):
        self.setup_user()

        with self.skip_check_course_selection(current_contract=self.contract):
            response = self.client.post(self._url_task_history_ajax, {})

        self.assertEqual(200, response.status_code)
        data = json.loads(response.content)
        self.assertEqual('success', data['status'])
        self.assertEqual(0, data['total'])
        self.assertFalse(data['records'])

    def test_task_history_not_allowed_method(self):
        response = self.client.get(self._url_task_history_ajax)
        self.assertEqual(405, response.status_code)