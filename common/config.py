import os

APPIUM_SERVER = 'http://127.0.0.1:4723/wd/hub'
DEVICE_FARM = False
if DEVICE_FARM:
    DESIRED_CAPABILITIES = {}
else:
    DESIRED_CAPABILITIES = {
      "platformName": "iOS",
      "platformVersion": "11.2",
      "deviceName": "iPhone 7",
      "automationName": "XCUITest",
      "app": "/Users/adnanghaffar/Desktop/BaseLine/PortoProd_New.app_updated.zip"
    }
TEST_RAILS_API_KEY = "E5jmoNXyU30AKSqfgE1j-RKQGgYlQIT6/2BBY49cX"
TEST_RAILS = {
    "URL": "https://baseline.testrail.io/",
    "API": "E5jmoNXyU30AKSqfgE1j-RKQGgYlQIT6/2BBY49cX",
    "USER": "farhan@baselinetelematics.com",
    "PASSWORD": "Test1234",
    "PROJECT_ID": 2,
    "PROJECT_NAME": "BaseDrive - T+G",
}
SHOULD_LOG_ON_TEST_RAIL = True
