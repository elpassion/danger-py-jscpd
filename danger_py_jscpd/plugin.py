import subprocess

from danger_python.plugins import DangerPlugin

from danger_py_jscpd.report_parser import ReportParser, Duplication


class DangerJSCPD(DangerPlugin):
    def jscpd(self):
        result = subprocess.run(["which", "jscpd"], capture_output=True, text=True)
        if result.returncode == 1:
            self.fail("Could not find jscpd in current directory, pleas run command `npm install -g jscpd`")
        else:
            self.run_jspcd()

    def run_jspcd(self):
        subprocess.run(["jscpd", "."], capture_output=True, text=True)
        try:
            with open("/report/jscpd-report.json") as report:
                parser = ReportParser()
                duplications = parser.parse(report.read())
                if duplications:
                    formatted_duplications = "\n".join(map(self.format_duplication, duplications))
                    markdown_message = (
                        f"### JSCPD found {len(duplications)} clone(s)\n"
                        "| First | Second | - |\n"
                        "| ------------- | -------- | --- |\n"
                        f"{formatted_duplications}"
                    )
                    self.markdown(markdown_message)
        except OSError:
            self.fail("Could not find jscpd-report.json in /report directory")

    def format_duplication(duplication: Duplication) -> str:
        first = f"| {duplication.first_file.path}: {duplication.first_file.start}-{duplication.first_file.end}"
        second = f"{duplication.second_file.path}: {duplication.second_file.start}-{duplication.second_file.end}"
        third = ":warning: |"

        return " | ".join([first, second, third])
