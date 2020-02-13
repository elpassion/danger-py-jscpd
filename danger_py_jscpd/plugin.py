from danger_python.plugins import DangerPlugin


class DangerJSCPD(DangerPlugin):
    def jscpd(self):
        self.fail("test_message")
