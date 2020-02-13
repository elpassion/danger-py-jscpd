from dataclasses import dataclass
import json


@dataclass
class File:
    path: str
    start: int
    end: int


@dataclass
class Duplication:
    first_file: File
    second_file: File


class ReportParser:
    def parse(self, json_string: str) -> [Duplication]:
        content = json.loads(json_string)
        duplications = []

        for duplication in content["duplicates"]:
            if duplication["format"] == "python":
                first_file = self.parsed_file(duplication["firstFile"])
                second_file = self.parsed_file(duplication["secondFile"])
                duplications.append(Duplication(first_file=first_file, second_file=second_file))

        return duplications

    def parsed_file(self, file: dict) -> File:
        return File(path=file["name"], start=file["start"], end=file["end"])
