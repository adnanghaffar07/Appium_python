# coding=utf-8
from __future__ import absolute_import, print_function

import json
import os
import unittest
import sys


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from appium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait

from common import config
from common import testrail
from common.providers.login import LoginElem
from pages.dashboard import DashboardScreen
from pages.login import LoginScreen
from tests.base import BaseTest

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LoginTests(BaseTest, unittest.TestCase):
    driver = None
    wait = None
    case_id = None

    def __init__(self, *args, **kwargs):
        super(LoginTests, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Remote(config.APPIUM_SERVER, config.DESIRED_CAPABILITIES)
        cls.wait = WebDriverWait(cls.driver, 10)
        cls.login = LoginScreen(cls.wait, cls.driver)
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

    def test_001_C647_login_page_verify_text(self):
        """
        Verify texts on login page
        """
        self.case_id = '647'
        self.login.click_on_allow_notifications_alert()
        self.assertTrue(self.login.get_email_field())
        self.assertTrue(self.login.get_password_field())

    def test_002_C648_login_screen_logo_visible(self):
        """
        App logo should be visible
        """
        self.case_id = '648'
        self.login.click_on_allow_notifications_alert()
        self.assertTrue(self.login.get_app_logo())

    def test_003_C1069_login_with_empty_email_pwd(self):
        """
        Login to app with empty email/password
        """
        self.case_id = '1069'
        self.login.click_on_allow_notifications_alert()
        try:
            btn_found = self.login.get_login_button().is_enabled()
        except TimeoutException:
            btn_found = False
        self.assertFalse(btn_found, msg='Enter button was found')

    def test_004_C1070_login_with_invalid_email(self):
        """
        Login to app with invalid email
        """
        self.case_id = '1070'
        self.login.click_on_allow_notifications_alert()
        self.login.submit_login_form(LoginElem.invalid_email, LoginElem.password)
        try:
            btn_found = self.login.get_login_button().is_enabled()
        except TimeoutException:
            btn_found = False
        self.assertFalse(btn_found, msg='Enter button was found')

    def test_005_C1071_login_with_small_pwd(self):
        """
        Login to app with password less than 8 characters
        """
        self.case_id = '1071'
        self.login.click_on_allow_notifications_alert()
        self.login.submit_login_form(LoginElem.email, LoginElem.small_password)
        try:
            btn_found = self.login.get_login_button().is_enabled()
        except TimeoutException:
            btn_found = False
        self.assertFalse(btn_found, msg='Enter button was found')

    def test_006_C1072_login_with_invalid_pwd(self):
        """
        Login to app with invalid password
        """
        self.case_id = '1072'
        self.login.click_on_allow_notifications_alert()
        self.login.submit_login_form(LoginElem.email, LoginElem.invalid_password)
        try:
            btn_found = self.login.get_login_button().is_enabled()
        except TimeoutException:
            btn_found = False
        self.assertFalse(btn_found, msg='Enter button was found')

    def test_007_C651_login_valid_cred(self):
        """
        Login to app with valid credentials
        """
        self.case_id = '651'
        # Click on Notification Alert
        self.login.click_on_allow_notifications_alert()
        self.login.submit_login_form(LoginElem.email, LoginElem.password)
        try:
            btn = self.login.get_login_button()
            btn_found = btn.is_enabled()
            btn.click()
        except TimeoutException:
            btn_found = False
        self.assertTrue(btn_found, msg='Enter button was NOT found')
        self.login.click_on_allow_notifications_alert()
        self.dashboard.click_on_always_allow_alert()
        self.login.click_on_allow_notifications_alert()
        self.assertTrue(self.dashboard.get_dashboard_main_elem())

    # def test_008_C652_logout_and_verify_login_page(self):
    #     """
    #     Logout and verify login screen appears
    #     """
    #     self.case_id = '652'
    #     self.dashboard.click_on_left_menu()
    #     self.dashboard.click_on_settings()
    #     self.dashboard.click_on_logout()
    #     self.assertTrue(self.login.get_login_button())

    def test_009_C713_verify_facebook_login(self):
        """
        Verify login using facebook account
        """
        self.driver.quit()
        self.driver.start_session(config.DESIRED_CAPABILITIES)
        self.wait = WebDriverWait(self.driver, 10)
        self.dashboard = DashboardScreen(self.wait, self.driver)

        self.case_id = '713'
        self.login.click_on_allow_notifications_alert()
        self.login.login_with_facebook(LoginElem.fb_email, LoginElem.fb_password)
        self.login.click_on_allow_notifications_alert()
        self.dashboard.click_on_always_allow_alert()
        self.assertTrue(self.dashboard.get_dashboard_main_elem())
        self.dashboard.click_on_left_menu()
        self.dashboard.click_on_settings()
        self.dashboard.click_on_logout()
        self.assertTrue(self.login.get_login_button())

    # def test_010_verify_google_login(self):
    #     """
    #     Verify login using google account
    #     """
    #     pass

    def test_010_C1082_verify_forgot_pwd(self):
        """
        Verify forgot password
        """
        self.case_id = '1082'
        self.login.click_on_allow_notifications_alert()
        self.login.click_on_forgot_pwd()
        random_email = 'dummy{}@gmail.com'.format(int(time.time()))
        self.login.submit_forgot_pwd_form(random_email)
        self.login.click_on_submit_forgot_pwd_btn()
        self.assertTrue(self.login.get_text_after_forgot_pwd_submit())


if __name__ == '__main__':
    if os.path.exists('common/runs.json') and config.SHOULD_LOG_ON_TEST_RAIL:
        os.remove('common/runs.json')
    suite = unittest.TestLoader().loadTestsFromTestCase(LoginTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
