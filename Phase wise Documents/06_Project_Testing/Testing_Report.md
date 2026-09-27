# Phase 6 – Project Testing

## Existing Automated Tests

The repository contains `tests/test_api.py`.

The current test file covers:
- Root endpoint response
- Health endpoint response
- Document-generation API using a mocked generator
- Validation when the document type is empty

## Test Evidence Table

| Test ID | Test Area | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC-01 | Root endpoint | Returns HTTP 200 and LegalEase service information | To be recorded from execution | Pending |
| TC-02 | Health endpoint | Returns HTTP 200 and `ok` status | To be recorded from execution | Pending |
| TC-03 | Mocked generation | Returns generated document content | To be recorded from execution | Pending |
| TC-04 | Empty document type | Request is rejected with HTTP 422 | To be recorded from execution | Pending |
| TC-05 | Streamlit input | User can enter document details | To be recorded from execution | Pending |
| TC-06 | Document preview/editing | Generated content can be reviewed/edited | To be recorded from execution | Pending |
| TC-07 | TXT export | TXT output is produced | To be recorded from execution | Pending |
| TC-08 | DOCX export | DOCX output is produced | To be recorded from execution | Pending |
| TC-09 | PDF export | PDF output is produced | To be recorded from execution | Pending |

## Evidence
Add screenshots from the real application to `Screenshots/` after performing the corresponding tests.

Only mark a test as **Passed** after it has actually been executed and verified.
