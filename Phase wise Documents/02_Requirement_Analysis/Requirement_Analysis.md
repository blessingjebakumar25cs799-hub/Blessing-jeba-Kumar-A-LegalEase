# Phase 2 – Requirement Analysis

## Functional Requirements

1. Allow the user to select or enter a document type.
2. Accept party information.
3. Accept terms and conditions.
4. Accept an effective date.
5. Send the request to the backend generation API.
6. Generate document content using the Gemini integration.
7. Display the generated document.
8. Allow the user to edit the generated content.
9. Provide TXT, DOCX and PDF output.

## Non-Functional Requirements
- User-friendly interface
- Maintainable Python architecture
- Responsive document generation
- Secure handling of API credentials
- Professional document formatting

## Inputs
- Document type
- Parties involved
- Terms / conditions
- Effective date

## Outputs
- Generated document content
- Editable document preview
- TXT, DOCX and PDF files

## Technologies
Python, FastAPI, Streamlit, Google Gemini, python-docx, fpdf2, Pillow and pytest.

## Scope Note
LegalEase is a document-generation aid. Generated content should be reviewed appropriately and is not a substitute for professional legal advice.
