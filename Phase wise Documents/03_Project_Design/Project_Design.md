# Phase 3 – Project Design

## Architecture

The implemented project follows this flow:

```text
Streamlit Frontend
        |
        | POST /generate
        v
FastAPI Backend
        |
        v
Gemini Document Generator
        |
        v
Google Gemini

Generated document
   |       |       |
  TXT     DOCX     PDF
```

## Components

### Frontend
`frontend/app.py` provides the Streamlit interface for document selection, party details, terms, effective date, generation, preview/editing and downloads.

### Backend
The FastAPI application is implemented under `backend/`. The API exposes the generation workflow and health endpoint.

### AI Layer
`backend/ai_core/gemini_generator.py` contains the Gemini document-generation integration.

### Formatting
`backend/services/document_formatter.py` handles document formatting/export functionality.

## API
The main generation operation is `POST /generate`. The backend also provides a health endpoint.

## Existing Design Evidence
The repository root contains `ARCHITECTURE.md`, which is the detailed architecture reference for the implemented project. It remains at the root so the working application and its architecture documentation stay together.
