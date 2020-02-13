from danger_python.danger import Danger, Violation

from danger_py_jscpd import DangerJSCPD


def test_plugin_does_fail_with_test_message(danger: Danger):
    plugin = DangerJSCPD()
    plugin.jscpd()

    assert danger.results.fails == [Violation(message="test_message")]
