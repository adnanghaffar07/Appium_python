# coding=utf-8
import time
from selenium.common.exceptions import WebDriverException, TimeoutException

from tests.base import DriverMethods


class DashboardScreen(DriverMethods):
    def __init__(self, wait, driver):
        super(DashboardScreen, self).__init__(wait, driver)

    def get_dashboard_main_elem(self):
        return self.find_element_by_xpath('//XCUIElementTypeOther[@name="Dashboard"]')

    def click_on_left_menu(self):
        self.find_element_by_xpath('//XCUIElementTypeButton[@name=""]').click()

    def click_on_settings(self):
        retries = 3
        while retries:
            try:
                self.driver.tap([[250, 43]])
                if self.get_logout_btn():
                    break
            except:
                time.sleep(2)
                retries -= 1
        # self.find_element_by_xpath('//XCUIElementTypeOther[@name="Dashboard"]/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther[3]/XCUIElementTypeOther/XCUIElementTypeStaticText').click()
        # self.find_element_by_xpath('//XCUIElementTypeStaticText[@name=""]').click()
        # time.sleep(5)
        # self.driver.tap([[242, 43]])

    def get_logout_btn(self):
        return self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Sair"]')

    def click_on_logout(self):
        self.find_element_by_xpath('//XCUIElementTypeStaticText[@name="Sair"]').click()

    def click_on_always_allow_alert(self):
        try:
            return self.find_element_by_xpath('//XCUIElementTypeButton[@name="Always Allow"]').click()
        except TimeoutException:
            return None
