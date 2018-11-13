# coding=utf-8
import time
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from common import config
from tests.base import DriverMethods


class LoginScreen(DriverMethods):
    def __init__(self, wait, driver):
        super(LoginScreen, self).__init__(wait, driver)

    def click_on_allow_notifications_alert(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeButton[@name="Allow"]').click()
        except TimeoutException:
            return None

    def get_app_logo(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeImage')
        except TimeoutException:
            return False

    def get_email_field(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeTextField')
        except TimeoutException:
            return False

    def get_password_field(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeSecureTextField')
        except TimeoutException:
            return False

    def get_login_button(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeButton[@name="Entrar"]')
        except (NoSuchElementException, TimeoutException):
            return False

    def click_on_login_submit(self):
        self.find_element_by_xpath('//XCUIElementTypeButton[@name="Entrar"]').click()

    def submit_login_form(self, email, password):
        email_field = self.find_element_by_xpath('//XCUIElementTypeTextField')
        email_field.clear()
        try:
            email_field.set_value(email)
        except Exception as e:
            print(e)

        password_field = self.find_element_by_xpath("//XCUIElementTypeSecureTextField")
        password_field.clear()
        password_field.set_value(password)

    def click_on_forgot_pwd(self):
        self.driver.tap([[116, 471]])

    def submit_forgot_pwd_form(self, email):
        # email_field = self.find_element_by_xpath('//XCUIElementTypeTextField[@value="E-mail"]')
        email_field = self.find_element_by_xpath('//XCUIElementTypeTextField')
        email_field.clear()
        email_field.set_value(email)

    def click_on_submit_forgot_pwd_btn(self):
        self.find_element_by_xpath('//XCUIElementTypeButton[@name="Enviar"]').click()

    def get_text_after_forgot_pwd_submit(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Confira seu e-mail"]')
        except (NoSuchElementException, TimeoutException):
            return False

    def get_facebook_continue_button(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeButton[@name="Continue"]')
        except (NoSuchElementException, TimeoutException):
            return False

    def get_facebook_open_app_button(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeButton[@name="Open"]')
        except (NoSuchElementException, TimeoutException):
            return False

    def login_with_facebook(self, email, password):
        self.find_element_by_xpath('//XCUIElementTypeButton[@name=" Facebook"]').click()
        print('clicked on fb')
        fb_continue = self.get_facebook_continue_button()
        if fb_continue:
            fb_continue.click()
            self.get_facebook_open_app_button().click()
        else:
            email_field = self.find_element_by_xpath('//XCUIElementTypeTextField')
            email_field.clear()
            email_field.set_value(email)
            self.find_element_by_xpath('//XCUIElementTypeButton[@name="Next"]').click()

            password_field = self.find_element_by_xpath('//XCUIElementTypeSecureTextField')
            password_field.clear()
            password_field.set_value(password)
            self.find_element_by_xpath('//XCUIElementTypeButton[@name="Next"]').click()

            self.find_element_by_xpath('//XCUIElementTypeButton[@name="Log In"]').click()
            time.sleep(5)
            self.driver.tap([[188, 481]])
            time.sleep(5)
            self.driver.tap([[306, 376]])

    def login_with_google(self, email, password):
        self.find_element_by_xpath('//XCUIElementTypeButton[@name="Google"]').click()
        self.submit_login_form(email, password)
        self.find_element_by_xpath('//XCUIElementTypeButton[@name="Log In"]').click()
        time.sleep(5)
        self.driver.tap([[188, 481]])
        time.sleep(5)
        self.driver.tap([[306, 376]])

