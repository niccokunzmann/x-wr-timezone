"""This test converts example calendars"""

def test_input_to_output(to_standard, calendar_pair):
    output = to_standard(calendar_pair.input.as_icalendar())
    assert output == calendar_pair.output.as_icalendar(), calendar_pair.message

