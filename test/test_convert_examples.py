"""This test converts example calendars"""

def test_input_to_output(to_standard, calendar_pair):
    output = to_standard(calendar_pair.input)
    assert output.to_ical() == calendar_pair.raw_output, calendar_pair.message

