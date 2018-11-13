# coding=utf-8
from __future__ import absolute_import, print_function

import json
import os
import unittest
import sys
import time


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from appium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from common import config, CPF
from common import testrail
from common.providers.login import LoginElem
from common.providers.registration import RegistrationElem
from pages.dashboard import DashboardScreen
from pages.login import LoginScreen
from pages.registration import RegistrationScreen
from tests.base import BaseTest

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class RegistrationTests(BaseTest, unittest.TestCase):
    """
    C656 - Validate pop up message
    C1073 - Verify Register with invalid email format
    C1074 - Verify Register with invalid password format
    C1075 - Verify Login link in Register page
    """
    driver = None
    wait = None
    case_id = None
    should_log_in_test_rail = True

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Remote(config.APPIUM_SERVER, config.DESIRED_CAPABILITIES)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.login = LoginScreen(cls.wait, cls.driver)
        cls.reg = RegistrationScreen(cls.wait, cls.driver)
        cls.dashboard = DashboardScreen(cls.wait, cls.driver)
        if os.path.exists(os.path.join(project_path, 'common/runs.json')):
            with open(os.path.join(project_path, 'common/runs.json'), 'r') as run_file:
                cls.current_testrail_run = json.loads(run_file.read())
        elif config.SHOULD_LOG_ON_TEST_RAIL:
            cls.current_testrail_run = cls.add_run(config.TEST_RAILS['PROJECT_NAME'])
            testrail.write_run_id_to_file(cls.current_testrail_run)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_001_C653_verify_registration_page_exists(self):
        """
        Verify registration page opens
        """
        self.case_id = '653'
        self.login.click_on_allow_notifications_alert()
        self.reg.click_on_registration_link()
        self.assertTrue(self.reg.get_submit_btn())

    def test_002_C1073_verify_registration_invalid_email(self):
        """
        Verify registration page
        """
        self.case_id = '1073'
        self.login.click_on_allow_notifications_alert()
        self.reg.click_on_registration_link()
        self.reg.submit_registration_form(LoginElem.invalid_email, LoginElem.password)
        self.assertFalse(self.reg.get_submit_btn().is_enabled())

    def test_003_C1074_verify_registration_invalid_password(self):
        """
        Verify registration page
        """
        self.case_id = '1074'
        self.login.click_on_allow_notifications_alert()
        self.reg.click_on_registration_link()
        self.reg.submit_registration_form(LoginElem.email, LoginElem.invalid_password)
        self.assertFalse(self.reg.get_submit_btn().is_enabled())

    def test_004_C1075_register_new_user(self):
        """
        Verify registration page opens
        """
        self.case_id = '1075'
        self.reg.click_on_login_link()
        self.assertTrue(self.reg.get_registration_link())

    def test_005_C1654_register_new_user(self):
        """
        Verify registration page opens
        """
        self.case_id = '654'
        self.reg.click_on_registration_link()
        random_email = 'dummy{}@gmail.com'.format(int(time.time()))
        self.reg.submit_registration_form(random_email, LoginElem.password)
        self.reg.click_on_submit()
        # self.assertTrue(self.reg.get_registration_link())

    def test_006_C1077_verify_invalid_cpf(self):
        """
        Verify invalid cpf number on link to policy
        """
        self.case_id = '1077'
        self.reg.submit_cpf_screen(58740411841, RegistrationElem.dob)
        self.assertTrue(self.reg.get_error_dialog_after_cpf())
        self.reg.get_ok_btn_after_activation_form().click()
        # self.assertFalse(self.reg.get_ok_btn_after_activation_form().is_enabled())

    def test_007_C1078_verify_invalid_dob(self):
        """
        Verify Invalid DOB on link to policy
        """
        self.case_id = '1078'
        self.reg.submit_cpf_screen(CPF.generate(), RegistrationElem.invalid_dob)
        self.assertTrue(self.reg.get_error_dialog_after_cpf())
        self.reg.get_ok_btn_after_activation_form().click()
        # self.assertFalse(self.reg.get_ok_btn_after_activation_form().is_enabled())

    def test_008_C1079_verify_empty_cpf(self):
        """
        Verify Empty cpf and DOB on link to policy
        """
        self.case_id = '1079'
        self.reg.submit_cpf_screen('', RegistrationElem.invalid_dob)
        self.assertTrue(self.reg.get_error_dialog_after_cpf())
        self.reg.get_ok_btn_after_activation_form().click()
        # self.assertFalse(self.reg.get_ok_btn_after_activation_form().is_enabled())

    def test_009_C655_enter_activation_code_dob(self):
        """
        Enter Activation code and Date of Birth
        """
        self.case_id = '655'
        self.reg.submit_cpf_screen(CPF.generate(), RegistrationElem.dob)
        self.assertTrue(self.reg.get_confirmation_after_cpf())
        self.reg.get_ok_btn_after_activation_form().click()

    # def test_007_C657_accept_terms_conditions(self):
    #     """
    #     Scroll down and to accept the terms & conditions
    #     """
    #     self.case_id = '657'
    #     # self.driver.drag_and_drop()
    #     # self.driver.swipe()


# if __name__ == '__main__':
#     if os.path.exists('common/runs.json') and config.SHOULD_LOG_ON_TEST_RAIL:
#         print 'Removing File for Registration Tests...'
#         os.remove('common/runs.json')
#     suite = unittest.TestLoader().loadTestsFromTestCase(RegistrationTests)
#     unittest.TextTestRunner(verbosity=2).run(suite)
