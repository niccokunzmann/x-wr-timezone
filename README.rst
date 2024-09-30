X-WR-TIMEZONE
=============

.. image:: https://github.com/niccokunzmann/x-wr-timezone/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/niccokunzmann/x-wr-timezone/actions/workflows/tests.yml
   :alt: CI build and test status

.. image:: https://badge.fury.io/py/x-wr-timezone.svg
   :target: https://pypi.python.org/pypi/x-wr-timezone
   :alt: Python Package Version on Pypi

.. image:: https://img.shields.io/pypi/dm/x-wr-timezone.svg
   :target: https://pypi.python.org/pypi/x-wr-timezone#downloads
   :alt: Downloads from Pypi

.. image:: https://img.shields.io/opencollective/all/open-web-calendar?label=support%20on%20open%20collective
   :target: https://opencollective.com/open-web-calendar/
   :alt: Support on Open Collective


Some calendar providers introduce the non-standard ``X-WR-TIMEZONE`` parameter
to ICS calendar files.
Strict interpretations according to RFC 5545 ignore the ``X-WR-TIMEZONE``
parameter.
This causes the times of the events to differ from those
which make use of ``X-WR-TIMEZONE``.

This module aims to bridge the gap by converting calendars
using ``X-WR-TIMEZONE`` to a strict RFC 5545 calendars.
So, let's put our heads together and solve this problem for everyone!

Some features of the module are:

- Easy install with Python's ``pip``.
- Command line conversion of calendars.
- Piping of calendar files with ``wget`` or ``curl``.

Some of the requirements are:

- Calendars without ``X-WR-TIMEZONE`` are kept unchanged.
- Passing calendars twice to this module does not change them.

Install
-------

Install using ``pip``:

.. code:: shell

    python3 -m pip install x-wr-timezone

Install with ``apt``:

.. code:: shell

    sudo apt-get install python-x-wr-timezone

Support
-------

- `Donate using GitHub Sponsors <https://github.com/sponsors/niccokunzmann>`_
- `Donate using Open Collective <https://opencollective.com/open-web-calendar/>`_
- `Donate using thanks.dev <https://thanks.dev>`_

Command Line Usage
------------------

You can standardize the calendars using your command line interface.
The examples assume that ``in.ics`` is a calendar which may use
``X-WR-TIMEZONE``, whereas ``out.ics`` does not require ``X-WR-TIMEZONE``
for proper display.

.. code-block:: shell

    cat in.is | x-wr-timezone > out.ics
    x-wr-timezone in.ics out.ics
    curl https://example.org/in.ics | x-wr-timezone > out.ics
    wget -O- https://example.org/in.ics | x-wr-timezone > out.ics

You can get usage help on the command line:

.. code-block:: shell

    x-wr-timezone --help

Python
------

After you have installed the library, you can import it.

.. code:: python

    import x_wr_timezone

The function ``to_standard()`` converts an ``icalendar`` object.

.. code:: python

    x_wr_timezone.to_standard(an_icalendar)

Here is a full example which does about as much as this module is supposed to do:

.. code-block:: python

    import icalendar # installed with x_wr_timezone
    import x_wr_timezone

    with open("in.ics", 'rb') as file:
        calendar = icalendar.from_ical(file.read())
    new_calendar = x_wr_timezone.to_standard(calendar)
    # you could use the new_calendar variable now
    with open('out.ics', 'wb') as file:
        file.write(new_calendar.to_ical())


``to_standard(calendar, timezone=None)`` has these parameters:

- ``calendar`` is the ``icalendar.Calendar`` object.
- ``timezone`` is an optional time zone. By default, the time zone in
  ``calendar['X-WR-TIMEZONE']`` is used to check if the calendar needs
  changing.
  When ``timezone`` is not ``None`` however, ``calendar['X-WR-TIMEZONE']``
  will not be tested and it is assumed that the ``calendar`` should be
  changed as if ``calendar['X-WR-TIMEZONE']`` had the value of ``timezone``.
  This does not add or change the value of ``calendar['X-WR-TIMEZONE']``.
  You would need to do that yourself.
  ``timezone`` can be a string like ``"UTC"`` or ``"Europe/Berlin"`` or
  a ``pytz.timezone`` or something that ``datetime`` accepts as a time zone..
- Return value: The ``calendar`` argument is not modified at all. The calendar
  returned has the attributes and subcomponents of the ``calendar`` only
  changed and copied where needed to return the proper value. As such,
  the returned calendar might be identical to the one passed to the
  function as the ``calendar`` argument. Keep that in mind if you modify the
  return value.


Development
-----------

1. Clone the `repository <https://github.com/niccokunzmann/x-wr-timezone>`_ or its fork and ``cd x-wr-timezone``.
2. Optional: Install virtualenv and Python3 and create a virtual environment:

   .. code-block:: shell

       pip install virtualenv
       virtualenv -p python3 ENV
       source ENV/bin/activate # you need to do this for each shell

3. Install the packages and this module so it can be edited:

   .. code-block:: shell

       pip install -r test-requirements.txt -e .

4. Run the tests:

   .. code-block:: shell

       pytest

To test all functions:

   .. code-block:: shell

       pytest --x-wr-timezone all

Testing with ``tox``
********************

You can use ``tox`` to test the package in different Python versions.

.. code-block:: shell

    tox

This tests all the different functionalities:

.. code-block:: shell

    tox -- --x-wr-timezone all

New Releases
------------

To release new versions,

1. edit the Changelog Section
2. edit setup.py, the ``__version__`` variable
3. create a commit and push it
4. Wait for `CI tests <https://github.com/niccokunzmann/x-wr-timezone/actions/workflows/tests.yml>`_ to finish the build.
5. run

   .. code-block:: shell

       python3 setup.py tag_and_deploy
6. notify the issues about their release

Testing
*******

This project's development is driven by tests.
Tests assure a consistent interface and less knowledge lost over time.
If you like to change the code, tests help that nothing breaks in the future.
They are required in that sense.
Example code and ics files can be transferred into tests and speed up fixing bugs.

You can view the tests in the `test folder
<https://github.com/niccokunzmann/x-wr-timezones/tree/main/test>`_.
If you have a calendar ICS file for which this library does not
generate the desired output, you can add it to the ``test/calendars``
folder and write tests for what you expect.
If you like, `open an issue <https://github.com/niccokunzmann/x-wr-timezone/issues>`_ first, e.g. to discuss the changes and
how to go about it.

Changelog
---------

- v1.0.0

  - Use `zoneinfo` instead of `pytz`
  - Test compatibility with `pytz` and `zoneinfo` as argument to `to_standard`
  - Remove `pytz` as a dependency
  - Add `tzdata` as a dependency
  - Add typing
  - Update Python versions

- v0.0.7

  - Rename master branch to main
  - Use proper SPDX license ID
  - Test Python 3.12

- v0.0.6

  - Obsolete Python 3.7
  - Support Python 3.11
  - Fix localization issue for pytz when datetime has no timezone
  - Run tests on GitHub Actions
  - Require icalendar 5.0.11 for tests
  - Fix pytz localization issue when dateime is not in UTC and has no time zone.

- v0.0.5

  - Revisit README and CLI and fix spelling mistakes.
  - Modified behavior to treat events without time zone found in a calendar using the X-WR-TIMEZONE property, see `Pull Request 7 <https://github.com/niccokunzmann/x-wr-timezone/pull/7>`__
- v0.0.4

  - Test automatic deployment with Gitlab CI.
- v0.0.3

  - Use ``tzname()`` function of ``datetime`` to test for UTC. This helps support zoneinfo time zones.
  - Split up visitor class and rename it to walker.
- v0.0.2

  - Implement the ``timezone`` argument.
  - Do not modify the value of the ``calendar`` argument and only copy it where needed.
- v0.0.1

  - Initial release supports DTSTART, DTEND, EXDATE, RDATE, RECURRENCE-ID attributes of events.
  - Command line interface as ``x-wr-timezone``.

Related Work
------------

This module was reated beause of these issues:

- `icalendar#343 <https://github.com/collective/icalendar/issues/343>`__
- `python-recurring-ical-events#71 <https://github.com/niccokunzmann/python-recurring-ical-events/issues/71>`__

Related Software
----------------

This module uses the ``icalendar`` library for parsing calendars.
This library is used by ``python-recurring-ical-events``
to get events at specific dates.

License
-------

This software is licensed under LGPLv3, see the LICENSE file.
