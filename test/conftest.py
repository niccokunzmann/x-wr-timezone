"""Test and fixture initialization."""
import icalendar
import pytest
import sys
import os

HERE = os.path.dirname(__file__)
REPO = os.path.dirname(HERE)

sys.path.append(REPO)

CALENDARS_FOLDER = os.path.join(HERE, "calendars")

NAME_END_INPUT = ".in"
NAME_END_OUTPUT = ".out"

calendars = {} # name: calendar

class TestCalendar:
    """A calendar in the test folder."""

    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        """Return the nicely readable id of the calendar."""
        name = os.path.basename(self.path)
        name = os.path.splitext(name)[0]
        return name.replace("-", " ")

    def is_input(self):
        """Whether this is a calendar which is used as an input for to_standard()."""
        return self.name.endswith(NAME_END_INPUT)

    def get_corrected_output_name(self):
        assert self.is_input(), "Only input calendars can have an output."
        return self.name[:len(self.name) - len(NAME_END_INPUT)] + NAME_END_OUTPUT

    def has_corrected_output(self):
        """Whether this has a calendar resulting from to_standard()."""
        return self.get_corrected_output_name() in calendars

    def get_corrected_output(self):
        """Return the corrected output of to_standard() for this calendar.

        KeyError if absent."""
        return calendars[self.get_corrected_output_name()]

    def __repr__(self):
        return "<{}>".format(self.id)

    def as_bytes(self):
        with open(self.path, "rb") as file:
            return file.read()

    def as_icalendar(self):
        return icalendar.Calendar.from_ical(self.as_bytes())

for calendar_file in os.listdir(CALENDARS_FOLDER):
    calendar_path = os.path.join(CALENDARS_FOLDER, calendar_file)
    calendar = TestCalendar(calendar_path)
    calendars[calendar.name] = calendar

class CalendarPair:
    """A pair of input and output calendars."""

    def __init__(self, input, output):
        self.input = input
        self.output = output

    @property
    def message(self):
        return self.input.as_icalendar().get("X-WR-CALNAME",
            "Pair of {} + {}".format(self.input.name, NAME_END_OUTPUT))

    def __repr__(self):
        return "<{}+{}>".format(self.input.name, NAME_END_OUTPUT)

# for parametrizing fixtures, see https://docs.pytest.org/en/latest/fixture.html#parametrizing-fixtures
@pytest.fixture(params=[calendar for calendar in calendars.values() if calendar.is_input() and calendar.has_corrected_output()])
def calendar_pair(request):
    return CalendarPair(request.param, request.param.get_corrected_output())

@pytest.fixture()
def to_standard():
    """Skip a test because it needs to be written first."""
    import x_wr_timezone
    return x_wr_timezone.to_standard

@pytest.fixture()
def todo():
    """Skip a test because it needs to be written first."""
    pytest.skip("This test is not yet implemented.")
