# How to run Assignment 2 tests in VS Code

1. Open the `INT6181_Assignment2_Solution` folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Run these commands one at a time:

```bash
python problem1.py
python -m unittest test_problem2.py -v
python -m unittest test_problem3.py -v
python -m unittest test_problem4.py -v
python -m unittest test_problem5.py -v
```

On Windows, if `python` is not recognized, try `py` instead of `python`.

## What the tests mean
- `... ok` means that test passed.
- `FAIL` means the program ran, but the result did not match the expected result.
- `ERROR` usually means an unexpected exception occurred.
- `Ran N tests ... OK` means all tests in that test file passed.

## Before submitting
- Review `bug_report.md` and make sure the screenshots you submit are genuine screenshots from your own VS Code test runs.
- Commit all changed files to your local Git repository.
- Run the tests again using the VS Code Testing panel, as the assignment requires.
