"""
Javascript test tasks
"""
import sys
from paver.easy import task, cmdopts
from pavelib.utils.test.suites import JsTestSuite
from pavelib.utils.envs import Env

__test__ = False  # do not collect


@task
@cmdopts([
    ("suite=", "s", "Test suite to run"),
    ("mode=", "m", "dev or run"),
    ("coverage", "c", "Run test under coverage"),
])
def test_js(options):
    """
    Run the JavaScript tests
    """
    mode = getattr(options, 'mode', 'run')

    if mode == 'run':
        suite = getattr(options, 'suite', 'all')
        coverage = getattr(options, 'coverage', False)
    elif mode == 'dev':
        suite = getattr(options, 'suite', None)
        coverage = False
    else:
        sys.stderr.write("Invalid mode. Please choose 'dev' or 'run'.")
        return

    if (suite != 'all') and (suite not in Env.JS_TEST_ID_KEYS):
        sys.stderr.write(
            "Unknown test suite. Please choose from ({suites})\n".format(
                suites=", ".join(Env.JS_TEST_ID_KEYS)
            )
        )
        return

    test_suite = JsTestSuite(suite, mode=mode, with_coverage=coverage)
    test_suite.run()


@task
@cmdopts([
    ("suite=", "s", "Test suite to run"),
    ("coverage", "c", "Run test under coverage"),
])
def test_js_run(options):
    """
    Run the JavaScript tests and print results to the console
    """
    setattr(options, 'mode', 'run')
    test_js(options)


@task
@cmdopts([
    ("suite=", "s", "Test suite to run"),
])
def test_js_dev(options):
    """
    Run the JavaScript tests in your default browsers
    """
    setattr(options, 'mode', 'dev')
    test_js(options)
