"""This test converts example calendars"""


def test_input_to_output(to_standard, calendar_pair):
    """Test the calendars which are a pait of input and output."""
    output = to_standard(calendar_pair.input.as_icalendar())
    assert output == calendar_pair.output.as_icalendar(), calendar_pair.message


def test_output_stays_the_same(to_standard, output_calendar):
    assert output_calendar.is_corrected_output()
    output = to_standard(output_calendar.as_icalendar())
    assert output == output_calendar.as_icalendar(), "A calendar that was modified one should stay as it is."
