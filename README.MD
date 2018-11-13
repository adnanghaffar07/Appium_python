# Steps to Create Tests Run on AWS Device Farm

-  Click on create a new run
- Upload or choose existing iOS application and click on next step
- Select Appium Python and upload zip'ed project
- By default it runs all the tests, if need to run specific test then click on edit and change this line for running only login tests
```sh
"bin/py.test tests/ --junit-xml $DEVICEFARM_LOG_DIR/junitreport.xml"
```
To
```sh
"bin/py.test tests/test_login.py --junit-xml $DEVICEFARM_LOG_DIR/junitreport.xml"
```
- Now click on next steps until there is button to start the run then tests will start running

# Run tests on local machine
```sh
$ pytest tests/
```