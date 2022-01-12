"""This test converts example calendars"""
import pytest


def assert_has_line(bytes, content, message):
    lines = message_lines = [line for line in bytes.decode("UTF-8").splitlines() if content[0] in line]
    for c in content:
        lines = [line for line in lines if c in line]
    assert lines, message + " One of these lines should contain {}: {}".format(content, message_lines)


def test_input_to_output(to_standard, calendar_pair):
    """Test the calendars which are a pair of input and output."""
    output = to_standard(calendar_pair.input.as_icalendar())
    assert output == calendar_pair.output.as_icalendar(), calendar_pair.message


def test_output_stays_the_same(to_standard, output_calendar):
    assert output_calendar.is_corrected_output()
    output = to_standard(output_calendar.as_icalendar())
    assert output == output_calendar.as_icalendar(), "A calendar that was modified one should stay as it is."


@pytest.mark.parametrize("calendar_name,content,message", [
    ("single-events-DTSTART-DTEND.in.ics", ("DTSTART", "TZID=America/New_York", ":20211222T120000"), "DTSTART should be converted.")
])
def test_conversion_changes_the_time_zone(to_standard, calendars, calendar_name, content, message):
    calendar = calendars[calendar_name]
    new_calendar = to_standard(calendar.as_icalendar())
    output_bytes = new_calendar.to_ical()
    assert_has_line(output_bytes, content, message)
