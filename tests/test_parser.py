from danger_py_jscpd.report_parser import ReportParser, Duplication, File


def test_parser_returns_duplications_for_python_format():
    with open("tests/fixtures/jscpd-report.json") as report:
        parser = ReportParser()
        duplications = parser.parse(report.read())

    assert len(duplications) == 9
    assert duplications[0] == Duplication(
        first_file=File(path="examples/babi_rnn.py", start=91, end=123),
        second_file=File(path="examples/babi_memnn.py", start=46, end=79)
    )
    assert duplications[-1] == Duplication(
        first_file=File(path="tests/test_model_pickling.py", start=87, end=95),
        second_file=File(path="tests/test_model_pickling.py", start=61, end=71)
    )
