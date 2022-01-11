"""Test and fixture initialization."""
import icalendar
import pytest

HERE = os.path.dirname(__file__)
REPO = os.path.dirname(HERE)

sys.path.append(REPO)

CALENDARS_FOLDER = os.path.join(HERE, "calendars")

ID_END_INPUT = "-in"
ID_END_OUTPUT = "-out"

calendars = {} # id: calendar

class TestCalendar:
    """A calendar in the test folder."""

    def __init__(self, path):
        self.path = path

    @property
    def id(self):
        """Return the nicely readable id of the calendar."""
        name = os.path.basename(self.path)
        name = os.path.splitext(name)[0]
        return name

    def is_input(self):
        """Whether this is a calendar which is used as an input for to_standard()."""
       return self.id.endswith(ID_END_INPUT)

    def get_corrected_output_id(self):
        assert self.is_input(), "Only input calendars can have an output."
        return self.id[:len(self.id) - len(ID_END_INPUT)] + ID_END_OUTPUT

    def has_corrected_output(self):
        """Whether this has a calendar resulting from to_standard()."""
        return self.get_corrected_output_id() in calendars

    def get_corrected_output(self):
        """Return the corrected output of to_standard() for this calendar.

        KeyError if absent."""
        return calendars[self.get_corrected_output_id()]


for calendar_file in os.listdir(CALENDARS_FOLDER):
    calendar_path = os.path.join(CALENDARS_FOLDER, calendar_file)
    calendar = TestCalendar(calendar_path)
    calendars[calendar.id] = calendar

# for parametrizing fixtures, see https://docs.pytest.org/en/latest/fixture.html#parametrizing-fixtures
@pytest.fixture(params=[calendar for calendar in calendars.values() if calendar.is_input() and calendar.has_corrected_output()])
def calendar_pair(request):
    return CaledarPair(request.param(), request.param().get_corrected_output())

@pytest.fixture()
def todo():
    """Skip a test because it needs to be written first."""
    pytest.skip("This test is not yet implemented.")
