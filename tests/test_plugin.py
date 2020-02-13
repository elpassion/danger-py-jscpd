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


def test_plugin_does_pass_when_jscpd_installed(danger: Danger):
    with patch("subprocess.Popen", new_callable=MockPopen) as popen:
        popen.set_command("which jscpd", returncode=0)
        popen.set_command("jscpd .", returncode=0)

        with Patcher() as patcher:
            patcher.fs.create_file("/report/jscpd-report.json", contents="")
            plugin = DangerJSCPD()
            plugin.jscpd()

    assert not danger.results.fails


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
