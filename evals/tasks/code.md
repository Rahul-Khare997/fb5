DOMAIN: code

TASK:
Write a Python 3.11 module `bookings.py` providing
`free_windows(bookings, day_start, day_end, min_minutes)`: given a list of (start, end)
timezone-aware datetime tuples for existing bookings (possibly overlapping, unsorted,
possibly extending beyond the day), return the list of (start, end) gaps within
[day_start, day_end) of at least min_minutes, sorted ascending. Include unit tests in the
same reply (pytest style, separate file content clearly labeled test_bookings.py).

RUBRIC:
1. Handles: empty bookings; bookings fully outside the day; overlapping and nested
   bookings; a booking spanning the whole day; zero-length bookings; min_minutes larger
   than the day. Each has a test asserting concrete expected values.
2. Rejects (raises ValueError with the offending value in the message): naive datetimes,
   end <= start bookings, day_end <= day_start, non-positive min_minutes. Tested.
3. Mixed-timezone input (e.g. one booking in UTC, another in UTC+5:30 for the same day)
   produces correct gaps; at least one test proves it.
4. No mutation of the input list; a test proves it.
5. Complete, runnable code: all imports present, no TODO stubs, no placeholder bodies,
   type hints on the public function.
6. Tests fail if the merge logic is broken (each asserts exact gap lists, not just counts
   or non-emptiness).
7. No print statements, no commented-out code, no docstring narrating the obvious; the
   docstring states the contract (boundary inclusivity, sort order, error conditions).
