import subprocess

from danger_python.plugins import DangerPlugin

from danger_py_jscpd.report_parser import ReportParser, Duplication
from typing import List, Optional
import os


class DangerJSCPD(DangerPlugin):
    def jscpd(self, paths: Optional[List[str]] = None, report_path: Optional[str] = None):
        paths = paths if paths else ["."]
        result = subprocess.run(["which", "jscpd"], capture_output=True, text=True)
        if result.returncode == 1:
            self.fail("Could not find jscpd in current directory, please run command `npm install -g jscpd`")
        else:
            self.__run_jspcd(paths, report_path)

    def __run_jspcd(self, paths: List[str], report_path: Optional[str]):
        reporter_parameter = ["-r", "json"]
        output_parameter = []
        if report_path:
            output_parameter.extend(["-o", report_path])

        command = ["jscpd"] + paths + reporter_parameter + output_parameter
        subprocess.run(command, capture_output=True, text=True)
        try:
            report_path = report_path if report_path else "report"
            report_file_path = os.path.join(report_path, "jscpd-report.json")
            with open(report_file_path) as report:
                parser = ReportParser()
                duplications = parser.parse(report.read())
                touched_files = set(self.danger.git.modified_files + self.danger.git.created_files)
                duplications = list(
                    filter(lambda d: d.first_file.path in touched_files or d.second_file.path in touched_files,
                           duplications))
                if duplications:
                    formatted_duplications = "\n".join(map(self.__format_duplication, duplications))
                    markdown_message = (
                        f"### JSCPD found {len(duplications)} clone(s)\n"
                        "| First | Second |\n"
                        "| ----- | ------ |\n"
                        f"{formatted_duplications}"
                    )
                    self.markdown(markdown_message)
        except OSError:
            self.fail("Could not find jscpd-report.json in report directory")

    def __format_duplication(self, duplication: Duplication) -> str:
        first = f"| {duplication.first_file.path}: {duplication.first_file.start}-{duplication.first_file.end}"
        second = f"{duplication.second_file.path}: {duplication.second_file.start}-{duplication.second_file.end} |"

        return " | ".join([first, second])
