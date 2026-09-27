# LegalEase – Project Report

## Abstract
LegalEase is an AI-powered legal document generator. It combines a Streamlit frontend, FastAPI backend and Google Gemini integration to assist users in generating legal-document drafts.

## Problem Statement
Preparing common legal documents manually can be time-consuming and may require familiarity with legal document structure.

## Proposed Solution
The application collects a document type, parties, terms and effective date, sends the request through the backend generation API, and presents the generated content for review/editing and download.

## Architecture
The repository's `ARCHITECTURE.md` documents the Streamlit → FastAPI → Gemini flow and TXT/DOCX/PDF outputs.

## Technology Stack
- Python
- FastAPI
- Streamlit
- Google Gemini
- python-docx
- fpdf2
- Pillow
- pytest

## Key Features
- AI-assisted legal document generation
- User input for document details
- Generated-document preview/editing
- TXT, DOCX and PDF output
- API health and validation handling

## Testing
The repository includes API tests for the root endpoint, health endpoint, mocked generation and validation. Additional manual test evidence should be recorded in Phase 6.

## Conclusion
LegalEase demonstrates an AI-assisted workflow for generating editable legal-document drafts through a simple web interface.
