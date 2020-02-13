import subprocess

from danger_python.plugins import DangerPlugin


class DangerJSCPD(DangerPlugin):
    def jscpd(self):
        result = subprocess.run(["which", "jscpd"], capture_output=True, text=True)
        if result.returncode == 1:
            self.fail("Could not find jscpd in current directory, pleas run command `npm install -g jscpd`")
