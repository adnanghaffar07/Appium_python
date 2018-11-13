# -*- coding: utf-8 -*-

import StringIO
import json
import os
import sys
import unittest

import tests.runner as HTMLTestRunner


# ----------------------------------------------------------------------
from common import config
from common import testrail
from tests.base import BaseTest
from tests.test_login import LoginTests
from tests.test_registration import RegistrationTests


def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)


def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')


# ------------------------------------------------------------------------


# This is the main test on HTMLTestRunner


class Test_HTMLTestRunner(BaseTest, unittest.TestCase):
    # def test0(self):
    #     self.suite = unittest.TestSuite()
    #     buf = StringIO.StringIO()
    #     runner = HTMLTestRunner.HTMLTestRunner(buf)
    #     runner.run(self.suite)
    #     # didn't blow up? ok.
    #     self.assert_('</html>' in buf.getvalue())

    def __init__(self, *args, **kwargs):
        self.current_testrail_run = self.add_run(config.TEST_RAILS['PROJECT_NAME'])
        testrail.write_run_id_to_file(self.current_testrail_run)
        super(Test_HTMLTestRunner, self).__init__(*args, **kwargs)

    def test_main(self):
        # Run HTMLTestRunner. Verify the HTML report.

        # suite of TestCases
        self.suite = unittest.TestSuite()
        self.suite.addTests([
            unittest.defaultTestLoader.loadTestsFromTestCase(LoginTests),
            unittest.defaultTestLoader.loadTestsFromTestCase(RegistrationTests),
        ])

        # Invoke TestRunner
        buf = StringIO.StringIO()
        # runner = unittest.TextTestRunner(buf)       #DEBUG: this is the unittest baseline
        runner = HTMLTestRunner.HTMLTestRunner(
            stream=buf,
            title='<Metra Tests>',
            description='This demonstrates the report output by HTMLTestRunner.'
        )
        runner.run(self.suite)

        # Define the expected output sequence. This is imperfect but should
        # give a good sense of the well being of the test.
        EXPECTED = u"""
Demo Test

>SampleTest0:

>SampleTest1:

>SampleTestBasic
>test_1<
>pass<
basic test

>test_2<
>pass<
basic test

>test_3<
>fail<
AssertionError: basic test

>test_4<
>error<
RuntimeError: basic test


>SampleTestHTML
>test_1<
>pass<
'the message is 5 symbols: \\x3C\\x3E\\x26\\"\\'\\n
plus the HTML entity string: [\\x26copy;] on a second line

>test_2<
>pass<
'the message is 5 symbols: \\x3C\\x3E\\x26\\"\\'\\n
plus the HTML entity string: [\\x26copy;] on a second line

>test_3<
>fail<
AssertionError: the message is 5 symbols: \\x3C\\x3E\\x26\\"\\'\\n
plus the HTML entity string: [\\x26copy;] on a second line

>test_4<
>error<
RuntimeError: the message is 5 symbols: \\x3C\\x3E\\x26\\"\\'\\n
plus the HTML entity string: [\\x26copy;] on a second line


>SampleTestLatin1
>test_1<
>pass<
the message is Ã¡Ã©Ã­Ã³Ãº

>test_2<
>pass<
the message is Ã¡Ã©Ã­Ã³Ãº

>test_3<
>fail<
AssertionError: the message is Ã¡Ã©Ã­Ã³Ãº

>test_4<
>error<
RuntimeError: the message is Ã¡Ã©Ã­Ã³Ãº


>SampleTestUnicode
>test_1<
>pass<
the message is \u8563

>test_2<
>pass<
the message is \u8563

>test_3<
>fail<
AssertionError: \\x3Cunprintable instance object\\x3E

>test_4<
>error<
RuntimeError: \\x3Cunprintable instance object\\x3E

Total
>19<
>10<
>5<
>4<
</html>
"""
        # check out the output
        byte_output = buf.getvalue()
        # output the main test output for debugging & demo
        print byte_output
        # HTMLTestRunner pumps UTF-8 output
        # output = byte_output.decode('utf-8')
        # self._checkoutput(output, EXPECTED)

    def _checkoutput(self, output, EXPECTED):
        i = 0
        for lineno, p in enumerate(EXPECTED.splitlines()):
            if not p:
                continue
            j = output.find(p, i)
            if j < 0:
                self.fail(safe_str('Pattern not found lineno %s: "%s"' % (lineno + 1, p)))
            i = j + len(p)


##############################################################################
# Executing this module from the command line
##############################################################################

import unittest

if __name__ == "__main__":
    if len(sys.argv) > 1:
        argv = sys.argv
    else:
        argv = ['test_HTMLTestRunner.py', 'Test_HTMLTestRunner']
    unittest.main(argv=argv)
    if os.path.exists('common/runs.json'):
        print 'Removing File for All tests...'
        os.remove('common/runs.json')
    # Testing HTMLTestRunner with HTMLTestRunner would work. But instead
    # we will use standard library's TextTestRunner to reduce the nesting
    # that may confuse people.
    # HTMLTestRunner.main(argv=argv)
