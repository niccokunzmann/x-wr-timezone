"""This checks that the vtimezone information is added to the calendar.

We add this information by default on the command line but we add
it on demand in the function.
"""

from zoneinfo import ZoneInfo
from icalendar import Calendar
import pytest

from x_wr_timezone import to_standard, get_timezone_component


@pytest.mark.parametrize("tz", [[], ["--add-timezone"]])
def test_cmd_add_timezone(cal_cmd, tz):
    """Create a calendar from the timezone information."""
    cal : Calendar = cal_cmd(tz + ["single-events-DTSTART-DTEND.in.ics"])
    timezones = cal.walk("VTIMEZONE")
    assert len(timezones) == 1
    assert timezones[0].tz_name == "America/New_York"

def test_cmd_no_timezone(cal_cmd):
    """Add option to not create a calendar from the timezone information."""
    cal : Calendar = cal_cmd(["--no-timezone", "single-events-DTSTART-DTEND.in.ics"])
    timezones = cal.walk("VTIMEZONE")
    assert len(timezones) == 0


def test_timezone_is_the_only_change(calendar_pair):
    """The subcomponents should be the same but we might get a timezone more."""
    cal = calendar_pair.input.as_icalendar()
    new_cal = to_standard(cal, add_timezone_component=True)
    l = len(new_cal.subcomponents)
    assert len(cal.subcomponents) in (l, l-1)


@pytest.mark.parametrize("add_timezone", [True, False])
def test_converted_event_time(calendars, add_timezone):
    """Check that the event time is converted."""
    calendar = calendars["single-events-DTSTART-DTEND.in.ics"]
    new_calendar = to_standard(calendar.as_icalendar(), add_timezone_component=add_timezone)
    assert new_calendar.events[0].start.tzinfo == ZoneInfo("America/New_York")
    assert new_calendar.timezones == [get_timezone_component(ZoneInfo("America/New_York"))] * add_timezone
    


def test_vtimezone_components_are_cached():
    """Check that the vtimezone component is cached."""
    assert get_timezone_component(ZoneInfo("Europe/Berlin")) is get_timezone_component(ZoneInfo("Europe/Berlin"))
