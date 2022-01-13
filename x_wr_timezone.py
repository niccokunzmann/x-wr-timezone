"""Bring calendars using X-WR-TIMEZONE into RFC 5545 form."""
import pytz
from icalendar.prop import vDDDTypes
import datetime

X_WR_TIMEZONE = "X-WR-TIMEZONE"

class TimeZoneChangingVisitor:
    """This implements a visitor pattern working on an icalendar object."""

    VALUE_ATTRIBUTES = ['DTSTART', 'DTEND']

    old_timezone = pytz.UTC

    def __init__(self, timezone):
        """Initialize the visitor with the new time zone."""
        self.new_timezone = timezone

    def visit(self, calendar):
        """Visit a calendar and change it to the time zone."""
        for event in calendar.walk('VEVENT'):
            self.visit_event(event)

    def visit_event(self, event):
        for attribute in self.VALUE_ATTRIBUTES:
            event[attribute] = self.visit_value(event[attribute])

    def visit_value(self, value):
        print("value", value.dt, value.to_ical())
        if isinstance(value.dt, datetime.datetime):
            dt = self.visit_datetime(value.dt)
            return vDDDTypes(dt)
        return value

    def visit_datetime(self, dt):
        if dt.tzinfo == self.old_timezone:
            return dt.astimezone(self.new_timezone)
        return dt

def to_standard(calendar):
    """Make a calendar that might use X-WR-TIMEZONE compatible with RFC 5545."""
    x_wr_timezone = calendar.get(X_WR_TIMEZONE, None)
    if x_wr_timezone is not None:
        new_timezone = pytz.timezone(x_wr_timezone)
        visitor = TimeZoneChangingVisitor(new_timezone)
        visitor.visit(calendar)
    return calendar
