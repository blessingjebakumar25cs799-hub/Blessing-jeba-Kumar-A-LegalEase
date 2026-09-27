import time

from google import genai
from google.genai import types

from backend.config import Settings
from backend.utils.text import sanitize_text


class GeminiDocumentGenerator:
    def __init__(self, settings: Settings):
        self.settings = settings

        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. "
                "Add it to your .env file."
            )

        self.client = genai.Client(
            api_key=settings.gemini_api_key
        )

    def _build_prompt(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:

        return f"""
You are the document-drafting engine for LegalEase.

Create a professional DRAFT {document_type}
from the user's supplied facts.

USER INPUT

Document type:
{document_type}

Parties:
{parties}

Terms / conditions:
{terms}

Effective date:
{effective_date}

REQUIREMENTS

1. Produce only the draft document, with no introductory chat.

2. Use clear legal-document headings and numbered sections.

3. Include a title, parties/recitals where appropriate,
   operative clauses, signatures, and a short review notice.

4. Preserve the supplied party names, roles, dates,
   and terms exactly in substance.

5. Do not invent addresses, monetary amounts,
   governing law, registration numbers, company details,
   deadlines, or other material facts that were not supplied.

6. Where a material legal detail is necessary but missing,
   insert a clearly marked placeholder such as:
   [GOVERNING LAW TO BE CONFIRMED]

7. Make the terms coherent, but do not claim that the
   result is legally valid in a particular jurisdiction.

8. Do not provide legal advice outside the document.

9. Use plain text headings suitable for DOCX/PDF conversion.

10. End with:

DRAFT - REVIEW BY A QUALIFIED LEGAL PROFESSIONAL RECOMMENDED.

Return only the document text.
""".strip()

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:

        prompt = self._build_prompt(
            document_type=document_type,
            parties=parties,
            terms=terms,
            effective_date=effective_date,
        )

        max_attempts = 3

        for attempt in range(max_attempts):

            try:
                response = self.client.models.generate_content(
                    model=self.settings.gemini_model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.2,
                        max_output_tokens=12000,
                    ),
                )

                text = getattr(response, "text", None)

                if not text:
                    raise RuntimeError(
                        "Gemini returned an empty response."
                    )

                return sanitize_text(text)

            except Exception as exc:

                error_text = str(exc)

                # Retry temporary Google service errors.
                if (
                    "503" in error_text
                    or "UNAVAILABLE" in error_text
                    or "high demand" in error_text.lower()
                ):

                    if attempt < max_attempts - 1:

                        wait_seconds = 2 ** attempt

                        time.sleep(wait_seconds)

                        continue

                    raise RuntimeError(
                        "Gemini is temporarily unavailable because "
                        "the service is experiencing high demand. "
                        "Please wait a few minutes and try again."
                    ) from exc

                # Do not retry authentication, model,
                # validation, or other permanent errors.
                raise