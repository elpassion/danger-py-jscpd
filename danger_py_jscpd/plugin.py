import subprocess

from danger_python.plugins import DangerPlugin


class DangerJSCPD(DangerPlugin):
    def jscpd(self):
        result = subprocess.run(["which", "jscpd"], capture_output=True, text=True)
        if result.returncode == 1:
            self.fail("Could not find jscpd in current directory, pleas run command `npm install -g jscpd`")
        else:
            subprocess.run(["jscpd", "."], capture_output=True, text=True)
            try:
                with open("/report/jscpd-report.json") as report:
                    pass
            except OSError:
                self.fail("Could not find jscpd-report.json in /report directory")



