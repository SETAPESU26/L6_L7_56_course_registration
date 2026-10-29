
import pytest
from course_registration import can_register, waitlist_position, late_fee


# Course registration tests
def test_regular_student_registers():
    assert can_register("regular", 20, 4, True) == "registered"


def test_prerequisites_missing():
    assert can_register("regular", 0, 3, False) == "prerequisites missing"


def test_credit_limit_exceeded():
    assert can_register("regular", 22, 4, True) == "credit limit exceeded"


def test_unknown_student_status():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("invalid", 0, 3, True)


def test_invalid_course_credits():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 0, 0, True)


# Waitlist tests
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0


def test_join_waitlist():
    assert waitlist_position(40, 40, 2) == 3


def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1


def test_invalid_capacity():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)


# Late fee tests
def test_no_late_fee():
    assert late_fee(0, 10, False) == 0


def test_fee_waived():
    assert late_fee(5, 10, True) == 0


def test_fee_within_seven_days():
    assert late_fee(5, 10, False) == 500


def test_fee_after_seven_days():
    assert late_fee(10, 10, False) == 800


def test_extra_fee_for_more_than_twenty_credits():
    assert late_fee(5, 21, False) == 750


def test_fee_capped_at_two_thousand():
    assert late_fee(30, 10, False) == 2000
