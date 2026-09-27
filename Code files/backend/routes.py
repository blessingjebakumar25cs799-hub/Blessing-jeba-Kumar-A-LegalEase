from fastapi import APIRouter, HTTPException

from backend.ai_core.gemini_generator import (
    GeminiDocumentGenerator,
)

from backend.config import get_settings

from backend.schemas import (
    DocumentRequest,
    DocumentResponse,
)


router = APIRouter()

settings = get_settings()


@router.get("/health")
def health() -> dict[str, str]:

    return {
        "status": "ok",
        "service": "LegalEase API",
    }


@router.post(
    "/generate",
    response_model=DocumentResponse,
)
def generate_document(
    request: DocumentRequest,
) -> DocumentResponse:

    try:

        generator = GeminiDocumentGenerator(
            settings
        )

        content = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date,
        )

        return DocumentResponse(
            document_type=request.document_type,
            content=content,
            model=settings.gemini_model,
        )

    except RuntimeError as exc:

        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=f"Document generation failed: {exc}",
        ) from exc