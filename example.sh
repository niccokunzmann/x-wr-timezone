#!/bin/bash

cIn="test/calendars/x-wr-timezone-not-present.in.ics"
cOut="test/calendars/x-wr-timezone-not-present.out.ics"
cTest="/tmp/x-wr-timezone-not-present.out.ics"

if ! x-wr-timezone "$cIn" "$cTest"; then
  echo "Error: x-wr-timezone did not run without error."
  exit 1
fi

# Cannot compare calendars at this point, tests will do that.

echo "Success!"

exit 0
