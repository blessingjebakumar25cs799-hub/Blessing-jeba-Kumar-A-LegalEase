import os
import sys
from pathlib import Path

# ============================================================
# PROJECT PATH
# ============================================================
ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# ============================================================
# IMPORTS
# ============================================================
import requests
import streamlit as st

from backend.services.document_formatter import (
    format_docx,
    format_pdf,
)


# ============================================================
# CONFIGURATION
# ============================================================
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000",
)

GENERATE_URL = f"{BACKEND_URL}/generate"


# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown(
    """
    <style>

        .main-title {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 18px;
            color: #666666;
            margin-bottom: 25px;
        }

        .warning-box {
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #e0c36c;
            background-color: #fff8dc;
            margin-top: 20px;
            margin-bottom: 20px;
        }

        .success-box {
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #8bc48b;
            background-color: #eef9ee;
            margin-top: 15px;
            margin-bottom: 15px;
        }

        .document-preview {
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #dddddd;
            background-color: #ffffff;
        }

        .small-text {
            font-size: 13px;
            color: #777777;
        }

        .edit-title {
            font-size: 24px;
            font-weight: 600;
            margin-top: 10px;
            margin-bottom: 5px;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================
if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""

if "edited_document" not in st.session_state:
    st.session_state.edited_document = ""

if "document_type" not in st.session_state:
    st.session_state.document_type = ""

if "model_name" not in st.session_state:
    st.session_state.model_name = ""

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:

    st.markdown("## ⚖️ LegalEase")

    st.markdown(
        "AI-Powered Legal Document Generator"
    )

    st.divider()

    st.markdown("### Document Details")

    document_options = [
        "Non-Disclosure Agreement",
        "Employment Agreement",
        "Rental Agreement",
        "Service Agreement",
        "Partnership Agreement",
        "Sale Agreement",
        "Loan Agreement",
        "Privacy Agreement",
        "Terms and Conditions",
        "Other",
    ]

    selected_document_type = st.selectbox(
        "Document Type",
        document_options,
    )

    if selected_document_type == "Other":

        document_type = st.text_input(
            "Enter document type",
            placeholder="Example: Consulting Agreement",
        )

    else:

        document_type = selected_document_type

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Example:\n"
            "Alice Smith (Party A)\n"
            "Example Technologies Ltd. (Party B)"
        ),
        height=130,
    )

    terms = st.text_area(
        "Terms / Conditions",
        placeholder=(
            "Describe the important terms and conditions.\n\n"
            "Example:\n"
            "- Confidential information must remain private.\n"
            "- Agreement remains effective for two years.\n"
            "- Information may only be used for the stated business purpose."
        ),
        height=220,
    )

    effective_date = st.date_input(
        "Effective Date"
    )

    st.divider()

    generate_button = st.button(
        "Generate Document",
        type="primary",
        use_container_width=True,
    )


# ============================================================
# MAIN HEADER
# ============================================================
st.markdown(
    '<div class="main-title">⚖️ LegalEase</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "AI-Powered Legal Document Generator"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# WARNING
# ============================================================
st.markdown(
    """
    <div class="warning-box">
        <strong>Important:</strong>
        LegalEase generates draft legal documents for review.
        Generated documents should be reviewed by a qualified legal
        professional before being used or signed.
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# GENERATE DOCUMENT
# ============================================================
if generate_button:

    if not document_type.strip():

        st.error(
            "Please select or enter a document type."
        )

    elif not parties.strip():

        st.error(
            "Please enter the parties involved."
        )

    elif not terms.strip():

        st.error(
            "Please enter the terms or conditions."
        )

    else:

        request_data = {
            "document_type": document_type.strip(),
            "parties": parties.strip(),
            "terms": terms.strip(),
            "effective_date": effective_date.isoformat(),
        }

        with st.spinner(
            "Generating your legal document..."
        ):

            try:

                response = requests.post(
                    GENERATE_URL,
                    json=request_data,
                    timeout=180,
                )

                if response.status_code == 200:

                    result = response.json()

                    generated_content = result.get(
                        "content",
                        "",
                    )

                    st.session_state.generated_document = (
                        generated_content
                    )

                    st.session_state.edited_document = (
                        generated_content
                    )

                    st.session_state.document_type = (
                        result.get(
                            "document_type",
                            document_type,
                        )
                    )

                    st.session_state.model_name = (
                        result.get(
                            "model",
                            "",
                        )
                    )

                    st.session_state.edit_mode = False

                    st.success(
                        "Document generated successfully."
                    )

                elif response.status_code == 422:

                    try:

                        error_data = response.json()

                        detail = error_data.get(
                            "detail",
                            "Invalid input.",
                        )

                    except Exception:

                        detail = "Invalid input."

                    st.error(
                        f"Validation error: {detail}"
                    )

                else:

                    try:

                        error_data = response.json()

                        detail = error_data.get(
                            "detail",
                            response.text,
                        )

                    except Exception:

                        detail = response.text

                    st.error(
                        f"Backend error ({response.status_code}): "
                        f"{detail}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI backend."
                )

                st.info(
                    "Make sure the backend is running with:\n\n"
                    "uvicorn backend.main:app "
                    "--reload --host 127.0.0.1 --port 8000"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The document generation request timed out."
                )

            except Exception as exc:

                st.error(
                    f"Unexpected error: {exc}"
                )


# ============================================================
# GENERATED DOCUMENT AREA
# ============================================================
if st.session_state.generated_document:

    st.divider()

    st.markdown(
        "## 📄 Generated Document"
    )

    if st.session_state.model_name:

        st.markdown(
            f'<div class="small-text">'
            f"Generated using: "
            f"{st.session_state.model_name}"
            f"</div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Preview")

    # ========================================================
    # EDIT BUTTON
    # ========================================================
    if not st.session_state.edit_mode:

        st.info(
            "Your document is ready. "
            "Click **✏️ Edit Document** if you want to make changes."
        )

        st.text_area(
            "Document Preview",
            value=st.session_state.generated_document,
            height=650,
            disabled=True,
            label_visibility="collapsed",
        )

        if st.button(
            "✏️ Edit Document",
            type="primary",
            use_container_width=True,
        ):

            st.session_state.edit_mode = True

            st.rerun()

    # ========================================================
    # EDIT MODE
    # ========================================================
    else:

        st.markdown(
            '<div class="edit-title">'
            "✏️ Edit Document"
            "</div>",
            unsafe_allow_html=True,
        )

        st.caption(
            "Make any changes you need in the document below."
        )

        edited_text = st.text_area(
            "Document Content",
            value=st.session_state.edited_document,
            height=650,
            label_visibility="collapsed",
        )

        col_save, col_cancel = st.columns(2)

        # ----------------------------------------------------
        # SAVE CHANGES
        # ----------------------------------------------------
        with col_save:

            if st.button(
                "💾 Save Changes",
                type="primary",
                use_container_width=True,
            ):

                st.session_state.edited_document = (
                    edited_text
                )

                st.session_state.generated_document = (
                    edited_text
                )

                st.session_state.edit_mode = False

                st.success(
                    "Changes saved successfully."
                )

                st.rerun()

        # ----------------------------------------------------
        # CANCEL
        # ----------------------------------------------------
        with col_cancel:

            if st.button(
                "↩️ Cancel",
                use_container_width=True,
            ):

                st.session_state.edit_mode = False

                st.rerun()


    # ========================================================
    # DOWNLOAD SECTION
    # ========================================================
    st.divider()

    st.markdown(
        "### 📥 Download Document"
    )

    st.caption(
        "Download the saved version of your document."
    )

    download_content = (
        st.session_state.edited_document
    )

    col1, col2, col3 = st.columns(3)

    # ========================================================
    # TXT
    # ========================================================
    with col1:

        st.download_button(
            label="📄 Download TXT",
            data=download_content,
            file_name="legalease_document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # ========================================================
    # DOCX
    # ========================================================
    with col2:

        try:

            docx_file = format_docx(
                download_content,
                st.session_state.document_type,
            )

            st.download_button(
                label="📝 Download DOCX",
                data=docx_file,
                file_name="legalease_document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

        except Exception as exc:

            st.error(
                f"Could not create DOCX: {exc}"
            )

    # ========================================================
    # PDF
    # ========================================================
    with col3:

        try:

            pdf_file = format_pdf(
                download_content,
                st.session_state.document_type,
            )

            st.download_button(
                label="📑 Download PDF",
                data=pdf_file,
                file_name="legalease_document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        except Exception as exc:

            st.error(
                f"Could not create PDF: {exc}"
            )


# ============================================================
# EMPTY STATE
# ============================================================
else:

    st.markdown(
        """
        ### 🚀 Get Started

        Enter the document details in the sidebar and click
        **Generate Document**.

        LegalEase will:

        1. Collect your document requirements.
        2. Send them to the FastAPI backend.
        3. Generate a draft using Gemini.
        4. Display the document for review.
        5. Let you edit the document.
        6. Save your changes.
        7. Download TXT, DOCX, or PDF versions.
        """
    )