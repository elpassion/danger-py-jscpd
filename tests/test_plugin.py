import pytest
from unittest.mock import patch

from danger_python.danger import Danger, Violation
from danger_python.plugins import DangerPlugin
from pyfakefs.fake_filesystem_unittest import Patcher
from testfixtures.popen import MockPopen

from danger_py_jscpd import DangerJSCPD


def test_plugin_inherits_from_danger_plugin():
    assert issubclass(DangerJSCPD, DangerPlugin)


def test_plugin_does_fail_when_jscpd_not_installed(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=1)

        plugin = DangerJSCPD()
        plugin.jscpd()

    message = "Could not find jscpd in current directory, pleas run command `npm install -g jscpd`"
    assert danger.results.fails == [Violation(message=message)]


def test_plugin_could_not_find_jscpd_report(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=0)
        popen.set_command("jscpd .", returncode=0)

        with Patcher():
            plugin = DangerJSCPD()
            plugin.jscpd()

    message = "Could not find jscpd-report.json in /report directory"
    assert danger.results.fails == [Violation(message=message)]


def test_plugin_founds_jscpd_report(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=0)
        popen.set_command("jscpd .", returncode=0)

        with open("tests/fixtures/jscpd-report.json") as report:
            with Patcher() as patcher:
                patcher.fs.create_file("/report/jscpd-report.json", contents=report.read())
                plugin = DangerJSCPD()
                plugin.jscpd()

    assert not danger.results.fails


def test_plugin_that_no_fails_and_markdowns_with_empty_jscpd_report(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=0)
        popen.set_command("jscpd .", returncode=0)

        with open("tests/fixtures/jscpd-report-empty.json") as report:
            with Patcher() as patcher:
                patcher.fs.create_file("/report/jscpd-report.json", contents=report.read())
                plugin = DangerJSCPD()
                plugin.jscpd()

    assert not danger.results.fails
    assert not danger.results.markdowns


@pytest.mark.parametrize("created_files", [["examples/babi_rnn.py"]])
@pytest.mark.parametrize("modified_files", [["examples/cifar10_resnet.py"]])
def test_plugin_that_generate_warn_and_markdown_with_valid_jscpd_report(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=0)
        popen.set_command("jscpd .", returncode=0)

        with open("tests/fixtures/jscpd-report.json") as report:
            with Patcher() as patcher:
                patcher.fs.create_file("/report/jscpd-report.json", contents=report.read())
                plugin = DangerJSCPD()
                plugin.jscpd()

    expected_markdown = (
        "### JSCPD found 3 clone(s)\n"
        "| First | Second | - |\n"
        "| ------------- | -------- | --- |\n"
        "| examples/babi_rnn.py: 91-123 | examples/babi_memnn.py: 46-79 | :warning: |\n"
        "| examples/babi_rnn.py: 124-131 | examples/babi_memnn.py: 80-87 | :warning: |\n"
        "| examples/cifar10_resnet.py: 344-355 | examples/cifar10_resnet.py: 248-259 | :warning: |"
    )

    assert danger.results.markdowns == [Violation(message=expected_markdown)]


@pytest.mark.parametrize("modified_files", [["tests/test_model_pickling.py"]])
def test_plugin_allows_to_customize_paths(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=0)
        popen.set_command("jscpd tests hello_world", returncode=0)

        with open("tests/fixtures/jscpd-report.json") as report:
            with Patcher() as patcher:
                patcher.fs.create_file("/report/jscpd-report.json", contents=report.read())
                plugin = DangerJSCPD()
                plugin.jscpd(paths=["tests", "hello_world"])

    expected_markdown = (
        "### JSCPD found 1 clone(s)\n"
        "| First | Second | - |\n"
        "| ------------- | -------- | --- |\n"
        "| tests/test_model_pickling.py: 87-95 | tests/test_model_pickling.py: 61-71 | :warning: |"
    )

    assert danger.results.markdowns == [Violation(message=expected_markdown)]


@pytest.mark.parametrize("modified_files", [["tests/test_model_pickling.py"]])
def test_plugin_allows_to_define_custom_report_path(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=0)
        popen.set_command("jscpd . -o custom/nested/", returncode=0)

        with open("tests/fixtures/jscpd-report.json") as report:
            with Patcher() as patcher:
                patcher.fs.create_file("custom/nested/jscpd-report.json", contents=report.read())
                plugin = DangerJSCPD()
                plugin.jscpd(report_path="custom/nested/")

    expected_markdown = (
        "### JSCPD found 1 clone(s)\n"
        "| First | Second | - |\n"
        "| ------------- | -------- | --- |\n"
        "| tests/test_model_pickling.py: 87-95 | tests/test_model_pickling.py: 61-71 | :warning: |"
    )

    assert danger.results.markdowns == [Violation(message=expected_markdown)]
