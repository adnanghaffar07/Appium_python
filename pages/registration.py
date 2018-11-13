# coding=utf-8
import time
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from tests.base import DriverMethods


class RegistrationScreen(DriverMethods):
    def __init__(self, wait, driver):
        super(RegistrationScreen, self).__init__(wait, driver)

    def click_on_registration_link(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Cadastrar"]').click()
        except TimeoutException:
            return None

    def get_registration_link(self):
        return self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Cadastrar"]')

    def submit_registration_form(self, email, password):
        email_field = self.find_element_by_xpath('//XCUIElementTypeTextField')
        email_field.clear()
        email_field.set_value(email)

        password_field = self.find_element_by_xpath("//XCUIElementTypeOther[3]/XCUIElementTypeSecureTextField")
        password_field.clear()
        password_field.set_value(password)

        password_field2 = self.find_element_by_xpath("//XCUIElementTypeOther[4]/XCUIElementTypeSecureTextField")
        password_field2.clear()
        password_field2.set_value(password)

    def click_on_submit(self):
        self.find_element_by_xpath('//XCUIElementTypeButton[@name="Cadastrar"]').click()

    def get_submit_btn(self):
        return self.find_element_by_xpath('//XCUIElementTypeButton[@name="Cadastrar"]')

    def submit_cpf_screen(self, cpf, data):
        cpf_field = self.find_element_by_xpath('//XCUIElementTypeOther[3]/XCUIElementTypeTextField')
        cpf_field.clear()
        cpf_field.set_value(cpf)

        data_field = self.find_element_by_xpath('//XCUIElementTypeOther[4]/XCUIElementTypeTextField')
        data_field.clear()
        data_field.set_value(data)

        self.find_element_by_xpath('//XCUIElementTypeButton[@name="Enviar"]').click()

    def get_submit_activation_btn(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeButton[@name="Enviar"]')
        except TimeoutException:
            return None

    def get_ok_btn_after_activation_form(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeButton[@name="OK"]')
        except TimeoutException:
            return None

    def click_on_login_link(self):
        self.find_element_by_xpath('//XCUIElementTypeTextField').click()
        self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Acessar"]').click()

    def get_confirmation_after_cpf(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Parabéns!"]')
        except:
            return None

    def get_error_dialog_after_cpf(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Erro"]')
        except:
            return None

    def click_on_accept_agreement(self):
        self.find_element_by_xpath('//XCUIElementTypeButton[@name="Aceitar"]').click()

    def click_on_btn_after_agreement_alert(self):
        self.find_element_by_xpath('(//XCUIElementTypeButton[@name="Pular"])[1]').click()

