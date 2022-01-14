# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Bring calendars using X-WR-TIMEZONE into RFC 5545 form."""
import sys
import pytz
from icalendar.prop import vDDDTypes, vDDDLists
import datetime
import icalendar

X_WR_TIMEZONE = "X-WR-TIMEZONE"

class TimeZoneChangingVisitor:
    """This implements a visitor pattern working on an icalendar object."""

    VALUE_ATTRIBUTES = ['DTSTART', 'DTEND', 'RDATE', 'RECURRENCE-ID', 'EXDATE']

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
            value = event.get(attribute)
            if value is not None:
                event[attribute] = self.visit_value(value)

    def visit_value_default(self, value):
        """Default method for visiting a value type."""
        return value


    def visit_value(self, value):
        """Visit a value type."""
        name = "visit_value_" + type(value).__name__
        visit = getattr(self, name, self.visit_value_default)
        return visit(value)

    def visit_value_list(self, l):
        """Visit a list of values."""
        return list(map(self.visit_value, l))

    def visit_value_vDDDLists(self, l):
        dts = [self.visit_value(ddd.dt) for ddd in l.dts]
        return vDDDLists(dts)

    def visit_value_vDDDTypes(self, value):
        """Visit an icalendar value type"""
        dt = self.visit_value(value.dt)
        return vDDDTypes(dt)

    def visit_value_datetime(self, dt):
        """Visit a datetime.datetime object."""
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

def main():
    """x-wr-timezone converts ICSfiles with X-WR-TIMEZONE to use RFC 5545 instead.

    Convert input:

        cat in.ics | x-wr-timezone > out.ics
        wget -O- https://example.org/in.ics | x-wr-timezone > out.ics
        curl https://example.org/in.ics | x-wr-timezone > out.ics

    Convert files:

        x-wr-timezone in.ics out.ics

    Get help:

        x-wr-timezone --help

    For bug reports, code and questions, visit the projet page:

        https://github.com/niccokunzmann/x-wr-timezone

    License: LPGLv3+
    """
    if len(sys.argv) == 1:
        in_file = getattr(sys.stdin, "buffer", sys.stdin)
        out_file = getattr(sys.stdout, "buffer", sys.stdout)
    elif len(sys.argv) == 3:
        in_file = open(sys.argv[1], 'rb')
        out_file = open(sys.argv[2], 'wb')
    else:
        sys.stdout.write(main.__doc__)
        return 0
    input = in_file.read()
    calendar = icalendar.Calendar.from_ical(input)
    output = to_standard(calendar).to_ical()
    out_file.write(output)
    return 0
