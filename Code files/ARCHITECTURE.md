# LegalEase Architecture

```text
                    ┌─────────────────────┐
                    │     Streamlit       │
                    │      Frontend       │
                    └──────────┬──────────┘
                               │
                               │ POST /generate
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │       Backend       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Gemini Generator    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Google Gemini    │
                    └─────────────────────┘


Generated document
        │
        ├──────────────► TXT
        │
        ├──────────────► DOCX
        │
        └──────────────► PDF