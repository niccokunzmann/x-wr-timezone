"""Test and fixture initialization."""
import x_wr_timezone
import icalendar
import pytest
import sys
import os
import tempfile
import subprocess

HERE = os.path.dirname(__file__)
REPO = os.path.dirname(HERE)

sys.path.append(REPO)

CALENDARS_FOLDER = os.path.join(HERE, "calendars")

NAME_END_INPUT = ".in"
NAME_END_OUTPUT = ".out"
EXECUTABLE = 'x-wr-timezone'

example_calendars = {} # name: calendar

class TestCalendar:
    """A calendar in the test folder."""

    def __init__(self, path):
        self.path = path

    @property
    def filename(self):
        return os.path.basename(self.path)

    @property
    def filename_without_ending(self):
        return os.path.splitext(self.filename)[0]

    @property
    def name(self):
        """Return the nicely readable id of the calendar."""
        return self.filename_without_ending.replace("-", " ")

    def is_input(self):
        """Whether this is a calendar which is used as an input for to_standard()."""
        return self.name.endswith(NAME_END_INPUT)

    def is_corrected_output(self):
        """Whether this is a calendar which would be a result of to_standard()."""
        return self.name.endswith(NAME_END_OUTPUT)

    def get_corrected_output_name(self):
        assert self.is_input(), "Only input calendars can have an output."
        return self.name[:len(self.name) - len(NAME_END_INPUT)] + NAME_END_OUTPUT

    def has_corrected_output(self):
        """Whether this has a calendar resulting from to_standard()."""
        return self.get_corrected_output_name() in example_calendars

    def get_corrected_output(self):
        """Return the corrected output of to_standard() for this calendar.

        KeyError if absent."""
        return example_calendars[self.get_corrected_output_name()]

    def __repr__(self):
        return "<{}>".format(self.name)

    def as_bytes(self):
        with open(self.path, "rb") as file:
            return file.read()

    def as_icalendar(self):
        return icalendar.Calendar.from_ical(self.as_bytes())

    def to_ical(self):
        return self.as_icalendar().to_ical()

for calendar_file in os.listdir(CALENDARS_FOLDER):
    calendar_path = os.path.join(CALENDARS_FOLDER, calendar_file)
    calendar = TestCalendar(calendar_path)
    example_calendars[calendar.name] = calendar
    example_calendars[calendar.filename] = calendar
    example_calendars[calendar.filename_without_ending] = calendar

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
@pytest.fixture(params=[calendar for calendar in example_calendars.values() if calendar.is_input() and calendar.has_corrected_output()])
def calendar_pair(request):
    """A pair of input and output calendar examples from the test/calendars folder."""
    return CalendarPair(request.param, request.param.get_corrected_output())


@pytest.fixture(params=[calendar for calendar in example_calendars.values() if calendar.is_corrected_output()])
def output_calendar(request):
    """A TestCalendar ending with .out in from the test/calendars folder."""
    return request.param


def to_standard_cmd_stdio(calendar):
    """Use the command line and piping."""
    input = calendar.to_ical()
    output = subprocess.check_output([EXECUTABLE], input=input)
    return icalendar.Calendar.from_ical(output)


conversions = {
    "all": [x_wr_timezone.to_standard, to_standard_cmd_stdio],
    "fast": [x_wr_timezone.to_standard],
    "io": [to_standard_cmd_stdio],
}

@pytest.fixture(params=[x_wr_timezone.to_standard, to_standard_cmd_stdio])
def to_standard(request, pytestconfig):
    """Change the to_standard() function to test several different methods.

    Use:
    - fast - use x_wr_timezone.to_standard(...)
    - io - use cat ... > x-wr-timezone
    - file - use x-wr-timezone in.ics out.ics
    - all - all of the above
    """
    to_standard = request.param
    if to_standard not in conversions[pytestconfig.option.to_standard]:
        pytest.skip("Use --x-wr-timezone=all to ativate all tests.")
    return to_standard


def pytest_addoption(parser):
    group = parser.getgroup("x-wr-timezone")
    group.addoption(
        "--x-wr-timezone",
        action="store",
        dest="to_standard",
        choices=("all", "file", "io", "fast"),
        default="fast",
        metavar="MODE",
        help=to_standard.__doc__,
    )


@pytest.fixture()
def calendars():
    """A mapping of all TestCalendars in the test/calendars folder."""
    return example_calendars.copy()


@pytest.fixture()
def todo():
    """Skip a test because it needs to be written first."""
    pytest.skip("This test is not yet implemented.")
