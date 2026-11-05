# Lab 6 - Code (Line) Coverage Test Cases
# Name: Divya Gupta | SRN: PES2UG24CS901 | Section: K
# Module under test: course_registration.py

import pytest
from course_registration import can_register, waitlist_position, late_fee


# ---------- can_register ----------
def test_registered():
    assert can_register("regular", 20, 4, True) == "registered"

def test_unknown_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)

def test_invalid_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_credit_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"


# ---------- waitlist_position ----------
def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_invalid_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)

def test_waitlist_full():
    assert waitlist_position(40, 40, 10) == -1

def test_waitlist_next_position():
    assert waitlist_position(40, 40, 3) == 4


# ---------- late_fee ----------
def test_not_late_no_fee():
    assert late_fee(0, 18, False) == 0

def test_waiver_no_fee():
    assert late_fee(5, 18, True) == 0

def test_late_within_week_heavy_load():
    # 500 base + 250 surcharge for credits > 20
    assert late_fee(3, 22, False) == 750

def test_very_late_fee_capped():
    # 500 + (30-7)*100 = 2800 -> capped at 2000
    assert late_fee(30, 18, False) == 2000
