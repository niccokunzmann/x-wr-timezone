"""This checks that the vtimezone information is added to the calendar.

We add this information by default on the command line but we add
it on demand in the function.
"""

from icalendar import Calendar
import pytest


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
