"""Make sure the examples are what we want them to be"""

def test_calendars_are_the_same(Calendars):
    assert Calendars["single-event-x-wr-timezone-not-used.in"].as_icalendar() == \
        Calendars["single-event-x-wr-timezone-not-used.out"].as_icalendar()


def test_calendars_differ(Calendars):
    assert Calendars["single-events-DTSTART-DTEND.in"].as_icalendar() != \
        Calendars["single-events-DTSTART-DTEND.out"].as_icalendar()
