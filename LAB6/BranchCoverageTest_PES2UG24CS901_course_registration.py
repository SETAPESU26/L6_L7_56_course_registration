# Lab 6 - Branch Coverage Test Cases
# Name: Divya Gupta | SRN: PES2UG24CS901 | Section: K
# Module under test: course_registration.py
# Every if-condition below is exercised on both its True and False side.

import pytest
from course_registration import can_register, waitlist_position, late_fee


# ======================= can_register =======================
# status valid/invalid, credits valid/invalid, prereqs met/not met,
# credit limit exceeded/within (incl. exact boundary) for every status

def test_unknown_status_raises():
    with pytest.raises(ValueError, match="unknown status"):
        can_register("alumni", 10, 4, True)

def test_zero_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("regular", 10, 0, True)

def test_negative_course_credits_raises():
    with pytest.raises(ValueError, match="invalid course credits"):
        can_register("honors", 10, -3, True)

def test_prerequisites_missing():
    assert can_register("regular", 10, 4, False) == "prerequisites missing"

def test_regular_registered():
    assert can_register("regular", 10, 4, True) == "registered"

def test_regular_exact_limit_registered():
    assert can_register("regular", 20, 4, True) == "registered"   # 24 == 24

def test_regular_limit_exceeded():
    assert can_register("regular", 21, 4, True) == "credit limit exceeded"

def test_probation_registered():
    assert can_register("probation", 12, 4, True) == "registered"  # 16 == 16

def test_probation_limit_exceeded():
    assert can_register("probation", 14, 4, True) == "credit limit exceeded"

def test_honors_registered():
    assert can_register("honors", 24, 4, True) == "registered"     # 28 == 28

def test_honors_limit_exceeded():
    assert can_register("honors", 26, 4, True) == "credit limit exceeded"


# ===================== waitlist_position =====================
# capacity valid/invalid, seat available/not, waitlist full/not full

def test_zero_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, 0, 0)

def test_negative_capacity_raises():
    with pytest.raises(ValueError, match="invalid capacity"):
        waitlist_position(10, -5, 0)

def test_seat_available():
    assert waitlist_position(30, 40, 0) == 0

def test_class_full_empty_waitlist():
    assert waitlist_position(40, 40, 0) == 1

def test_class_full_waitlist_partial():
    assert waitlist_position(40, 40, 9) == 10   # boundary: 9 < 10

def test_waitlist_full_boundary():
    assert waitlist_position(40, 40, 10) == -1  # boundary: 10 >= 10

def test_over_enrolled_waitlist_full():
    assert waitlist_position(45, 40, 15) == -1


# ========================= late_fee =========================
# days_late <=0 / >0, waiver / no waiver, <=7 / >7 days,
# credits >20 / <=20, fee >2000 (capped) / <=2000

def test_not_late_no_fee():
    assert late_fee(0, 18, False) == 0

def test_early_negative_days_no_fee():
    assert late_fee(-2, 22, False) == 0

def test_waiver_no_fee():
    assert late_fee(5, 18, True) == 0

def test_within_week_normal_load():
    assert late_fee(3, 18, False) == 500

def test_exactly_seven_days_normal_load():
    assert late_fee(7, 20, False) == 500        # boundary: 7 <= 7, credits 20 not > 20

def test_within_week_heavy_load():
    assert late_fee(3, 22, False) == 750

def test_after_week_normal_load():
    assert late_fee(10, 18, False) == 800       # 500 + 3*100

def test_after_week_heavy_load():
    assert late_fee(10, 22, False) == 1050      # 500 + 300 + 250

def test_fee_exactly_at_cap_not_capped():
    assert late_fee(22, 18, False) == 2000      # 500 + 15*100 = 2000

def test_fee_above_cap_is_capped():
    assert late_fee(30, 18, False) == 2000      # 2800 -> 2000

def test_heavy_load_pushes_over_cap():
    assert late_fee(21, 22, False) == 2000      # 1900 + 250 = 2150 -> 2000
