
import pytest
from course_registration import can_register, waitlist_position, late_fee


# can_register: both True and False outcomes of its conditions
@pytest.mark.parametrize(
    "status,current,course,prerequisites,expected",
    [
        ("regular", 20, 4, True, "registered"),
        ("probation", 12, 4, True, "registered"),
        ("honors", 24, 4, True, "registered"),
        ("regular", 0, 3, False, "prerequisites missing"),
        ("regular", 22, 4, True, "credit limit exceeded"),
        ("regular", 0, 3, True, "registered"),
    ],
)
def test_registration_branches(status, current, course, prerequisites, expected):
    assert can_register(status, current, course, prerequisites) == expected


@pytest.mark.parametrize(
    "status,course",
    [
        ("unknown", 3),
        ("regular", 0),
        ("regular", -1),
    ],
)
def test_registration_errors(status, course):
    with pytest.raises(ValueError):
        can_register(status, 0, course, True)


# waitlist_position: capacity, seats and waitlist-length branches
@pytest.mark.parametrize(
    "enrolled,capacity,length,expected",
    [
        (5, 10, 0, 0),
        (10, 10, 0, 1),
        (12, 10, 9, 10),
        (10, 10, 10, -1),
    ],
)
def test_waitlist_branches(enrolled, capacity, length, expected):
    assert waitlist_position(enrolled, capacity, length) == expected


def test_invalid_waitlist_capacity():
    with pytest.raises(ValueError):
        waitlist_position(5, 0, 0)


# late_fee: early returns, fee ranges, surcharge and cap
@pytest.mark.parametrize(
    "days,credits,waiver,expected",
    [
        (0, 10, False, 0),
        (-1, 10, False, 0),
        (5, 10, True, 0),
        (1, 10, False, 500),
        (7, 20, False, 500),
        (8, 20, False, 600),
        (8, 21, False, 850),
        (30, 10, False, 2000),
        (30, 21, False, 2000),
    ],
)
def test_late_fee_branches(days, credits, waiver, expected):
    assert late_fee(days, credits, waiver) == expected
