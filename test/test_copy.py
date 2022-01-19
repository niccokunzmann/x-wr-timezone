"""These tests check that the argument is not modified."""
from x_wr_timezone import to_standard
import pytest


@pytest.mark.parametrize("calendar_name,message", [
   ("x-wr-timezone-not-present.in.ics", "No X-WR-TIMEZONE no change"),
   ("rdate-hackerpublicradio.out.ics", "no change, same calendar"),
])
def test_no_change(calendars, calendar_name, message):
    """Test when calendars do not change."""
    calendar = calendars[calendar_name].as_icalendar()
    same_calendar = to_standard(calendar)
    assert same_calendar is calendar, message

def test_calendar_is_changed(calendars):
    """If X-WR-TIMEZONE changes the calendar, it should create a copy."""
    calendar = calendars["rdate-hackerpublicradio.in.ics"].as_icalendar()
    changed_calendar = to_standard(calendar)
    assert changed_calendar is not calendar


def test_components_are_not_altered(calendars):
    """The components of the calendar should be altered but originals left intact."""
    calendar = calendars["rdate-hackerpublicradio.in.ics"].as_icalendar()
    changed_calendar = to_standard(calendar)
    output_original = calendar.to_ical().decode("UTF-8")
    output_original_lines = output_original.splitlines()
    output_changed = changed_calendar.to_ical().decode("UTF-8")
    output_changed_lines = output_changed.splitlines()
    for original_line, new_line in zip(output_original_lines, output_changed_lines):
        print("o:\t", original_line, "\n\t", new_line)
    assert output_original_lines != output_changed_lines


def get_lines(calendar):
    output_changed = calendar.to_ical().decode("UTF-8")
    return output_changed.splitlines()


def filter_lines(calendar, content):
    return [line for line in get_lines(calendar) if content in line]


@pytest.mark.parametrize("calendar_name", [
    "rdate-hackerpublicradio.in.ics",
    "moved-event-RECURRENCE-ID.in.ics",
])
@pytest.mark.parametrize("property", "RDATE,BEGIN,BEGIN:CALENDAR,BEGIN:EVENT,END:EVENT,END:CALENDAR,DTSTART,DTEND,SUMMARY".split(","))
def test_components_all_in_there(calendars, calendar_name, property):
    """Make sure all components are there."""
    calendar = calendars[calendar_name].as_icalendar()
    l1 = filter_lines(calendar, property)
    changed_calendar = to_standard(calendar)
    l2 = filter_lines(calendar, property)
    l3 = filter_lines(changed_calendar, property)
    assert l1 == l2, "calendar itself should not have changed"
    assert len(l2) == len(l3), "no components should be added"


