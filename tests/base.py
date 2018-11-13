import time
import unittest
from datetime import datetime

from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from common import config
from common import testrail


class DriverMethods(object):

    def __init__(self, wait, driver):
        self.wait = wait
        self.driver = driver

    def find_element_by_ios_ui_automation(self, value):
        return self.wait.until(expected_conditions.visibility_of_element_located((MobileBy.IOS_UIAUTOMATION, value)))

    def find_elements_by_ios_ui_automation(self, value):
        return self.wait.until(expected_conditions.visibility_of_any_elements_located((MobileBy.IOS_UIAUTOMATION, value)))

    def find_element_by_xpath(self, xpath):
        # return self.wait.until(expected_conditions.visibility_of_element_located((By.XPATH, xpath)))
        return self.wait.until(expected_conditions.presence_of_element_located((By.XPATH, xpath)))

    def find_elements_by_xpath(self, xpath):
        return self.wait.until(expected_conditions.visibility_of_any_elements_located((By.XPATH, xpath)))

    def find_element_by_class_name(self, class_name):
        return self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, class_name)))

    def find_element_by_name(self, name):
        return self.wait.until(expected_conditions.visibility_of_element_located((By.NAME, name)))

    def find_elements_by_class_name(self, class_name):
        self.wait.until(expected_conditions.visibility_of_element_located((By.CLASS_NAME, class_name)))
        return self.driver.find_elements_by_class_name(class_name)

    def go_back(self):
        self.driver.tap([[67, 48]])


class BaseTest(object):
    client = None
    should_log_in_test_rail = False
    currentResult = None  # holds last result object passed to run method
    case_id = ''

    def setUp(self):
        pass

    # def tearDown(self):
    #     ok = self.currentResult.wasSuccessful()
    #     errors = self.currentResult.errors
    #     failures = self.currentResult.failures
    #     print ' All tests passed so far!' if ok else \
    #         ' %d errors and %d failures so far' % \
    #         (len(errors), len(failures))
    #     msg = "Test Passes" if ok else "Test Failed"
    #     if config.SHOULD_LOG_ON_TEST_RAIL:
    #         self.update_testrail(self.case_id, self.current_testrail_run['id'], ok, msg=msg)

    def run(self, result=None):
        self.currentResult = result  # remember result for use in tearDown
        unittest.TestCase.run(self, result)  # call superclass run method

    @classmethod
    def get_test_rail_client(cls):
        if cls.client:
            return cls.client
        cls.client = testrail.APIClient(config.TEST_RAILS['URL'])
        cls.client.user = config.TEST_RAILS['USER']
        cls.client.password = config.TEST_RAILS['PASSWORD']
        return cls.client

    def update_testrail(self, case_id, run_id, result_flag, msg=""):
        "Update TestRail for a given run_id and case_id"
        update_flag = False
        # Get the TestRail client account details
        client = self.get_test_rail_client()

        # Update the result in TestRail using send_post function.
        # Parameters for add_result_for_case is the combination of runid and case id.
        # status_id is 1 for Passed, 2 For Blocked, 4 for Retest and 5 for Failed
        status_id = 1 if result_flag is True else 5

        if run_id is not None:
            try:
                result = client.send_post(
                    'add_result_for_case/%s/%s' % (run_id, case_id),
                    {'status_id': status_id, 'comment': msg})
            except Exception as e:
                pass
                # print 'Exception in update_testrail() updating TestRail.'
                # print 'PYTHON SAYS: '
                # print e
            else:
                print('Updated test result for case: %s in test run: %s with msg:%s' % (case_id, run_id, msg))

        return update_flag

    @classmethod
    def get_project_id(cls, project_name):
        """Get the project ID using project name"""
        client = cls.get_test_rail_client()
        project_id = None
        projects = client.send_get('get_projects')
        for project in projects:
            if project['name'] == project_name:
                project_id = project['id']
                # project_found_flag=True
                break
        return project_id

    def get_run_id(self, test_run_name, project_name):
        """Get the run ID using test name and project name"""
        run_id = None
        client = self.get_test_rail_client()
        project_id = self.get_project_id(project_name)
        try:
            test_runs = client.send_get('get_runs/%s' % (project_id))
        except Exception as e:
            # print 'Exception in update_testrail() updating TestRail.'
            # print 'PYTHON SAYS: '
            # print e
            return None
        else:
            for test_run in test_runs:
                if test_run['name'] == test_run_name:
                    run_id = test_run['id']
                    break
            return run_id

    @classmethod
    def add_run(cls, project_name):
        client = cls.get_test_rail_client()
        project_id = cls.get_project_id(project_name)
        # print project_id
        test_run = client.send_post('add_run/%s' % project_id,
                                    {'name': '{} - {}'.format(project_name, datetime.today().strftime('%m-%d-%Y %X'))})
        return test_run
