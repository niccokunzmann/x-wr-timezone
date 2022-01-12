"""Make sure the examples are what we want them to be"""

def test_calendars_are_the_same(Calendars):
    assert Calendars["single-event-x-wr-timezone-not-used.in"].to_ical() == \
        Calendars["single-event-x-wr-timezone-not-used.out"].to_ical()


def test_calendars_differ(Calendars):
    assert Calendars["single-events-DTSTART-DTEND.in"].to_ical() != \
        Calendars["single-events-DTSTART-DTEND.out"].to_ical()
