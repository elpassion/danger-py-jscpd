from danger_python.danger import Danger, Violation
from danger_python.plugins import DangerPlugin

from danger_py_jscpd import DangerJSCPD


def test_plugin_inherits_from_danger_plugin(danger: Danger):
    assert issubclass(DangerJSCPD, DangerPlugin)
