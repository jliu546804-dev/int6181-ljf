# Bug Report — INT6181 Assignment 2

This report records bugs confirmed by tests and the corresponding fixes.

---

## Bug Report 1: Problem 4 — Back-to-back meetings incorrectly rejected

### 1. Program Under Test
- **File:** `problem4.py`
- **Class / Function:** `MeetingRoom.book()`

### 2. Failing Test Case
From `test_problem4.py`:

```python
def test_back_to_back_meetings_allowed(self):
    self.room.book("B01", "Morning meeting", 9, 10, 5)
    self.room.book("B02", "Next meeting", 10, 12, 4)
```

**Test Output / Error Message (before fix):**

```text
ValueError: Time slot [10, 12] conflicts with booking 'B01' [9, 10]
```

### 3. Root Cause Analysis
- **Expected Behavior:** Meetings ending and starting at the same hour are consecutive, not overlapping, so both bookings should succeed.
- **Actual Behavior:** The second booking was rejected as a conflict.
- **Root Cause:** The original conflict check used strict comparisons (`end_time < existing_start` and `start_time > existing_end`), so equal endpoints were treated as overlaps.

### 4. Code Fix & Diff
```diff
- if not (end_time < b["start_time"] or start_time > b["end_time"]):
+ if not (end_time <= b["start_time"] or start_time >= b["end_time"]):
```

---

## Bug Report 2: Problem 5 — Minimum and maximum aggregations reversed

### 1. Program Under Test
- **File:** `problem5.py`
- **Class / Function:** `clean_and_aggregate()`

### 2. Failing Test Case
From `test_problem5.py`:

```python
def test_aggregate_min_and_max(self):
    min_result = clean_and_aggregate(
        self.sample_sales, group_by="region", metric="sales", aggregation="min"
    )
    max_result = clean_and_aggregate(
        self.sample_sales, group_by="region", metric="sales", aggregation="max"
    )
    self.assertAlmostEqual(min_result["North"], 100.0)
```

**Test Output / Error Message (before fix):**

```text
AssertionError: 200.0 != 100.0 within 7 places (100.0 difference)
```

### 3. Root Cause Analysis
- **Expected Behavior:** `min` returns the smallest value in a group and `max` returns the largest.
- **Actual Behavior:** The `min` operation returned the largest value, while `max` returned the smallest.
- **Root Cause:** The calls to `min()` and `max()` were swapped in the two branches.

### 4. Code Fix & Diff
```diff
 elif agg_op == "min":
-    val = max(values)
+    val = min(values)
 elif agg_op == "max":
-    val = min(values)
+    val = max(values)
```

---

## Bug Report 3: Problem 5 — Empty input does not raise ValueError

### 1. Program Under Test
- **File:** `problem5.py`
- **Class / Function:** `clean_and_aggregate()`

### 2. Failing Test Case
From `test_problem5.py`:

```python
def test_empty_dataset_raises_value_error(self):
    with self.assertRaises(ValueError):
        clean_and_aggregate([], group_by="region", metric="sales")
```

**Test Output / Error Message (before fix):**

```text
AssertionError: ValueError not raised
```

### 3. Root Cause Analysis
- **Expected Behavior:** An empty records list should raise `ValueError`, as stated in the function documentation and test suite.
- **Actual Behavior:** The function returned an empty result dictionary without raising an exception.
- **Root Cause:** The function did not validate whether `records` was empty before aggregation.

### 4. Code Fix & Diff
```diff
+ if not isinstance(records, list):
+     raise TypeError("records must be a list")
+ if not records:
+     raise ValueError("records cannot be empty")
```

---

## Verification
The tests in `test_problem2.py`, `test_problem3.py`, `test_problem4.py`, and `test_problem5.py` were run after the fixes. Problem 1 doctests were also run. See the final test run for the pass/fail summary.
