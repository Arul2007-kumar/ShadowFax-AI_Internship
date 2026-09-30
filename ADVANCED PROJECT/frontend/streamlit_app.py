import streamlit as st
import requests
import os


# =============================
# Configuration
# =============================

API_URL = os.getenv("BACKEND_URL")


# =============================
# Page Configuration
# =============================

st.set_page_config(
    page_title="Production RAG Assistant",
    page_icon="🤖",
    layout="wide"
)


# =============================
# Title
# =============================

st.title("🤖 Production RAG Assistant")

st.write(
    "Upload a PDF, TXT, or Markdown document "
    "and ask questions based on its content."
)


# =============================
# Upload Section
# =============================

st.header("📄 Document Upload")

uploaded_file = st.file_uploader(
    "Choose a document",
    type=["pdf", "txt", "md"]
)


if uploaded_file is not None:

    st.info(
        f"Selected file: {uploaded_file.name}"
    )

    if st.button("🚀 Upload Document"):

        try:

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            with st.spinner(
                "Processing document..."
            ):

                response = requests.post(
                    f"{API_URL}/documents/upload",
                    files=files,
                    timeout=180
                )

            if response.status_code == 200:

                data = response.json()

                st.success(
                    "Document processed successfully! ✅"
                )

                # Store document information
                st.session_state[
                    "document_id"
                ] = data.get(
                    "document_id"
                )

                st.session_state[
                    "filename"
                ] = data.get(
                    "filename"
                )

                st.session_state[
                    "document_uploaded"
                ] = True

                # Show processing information

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Chunks",
                        data.get(
                            "chunks",
                            0
                        )
                    )

                with col2:

                    st.metric(
                        "Embeddings",
                        data.get(
                            "embeddings",
                            0
                        )
                    )

            else:

                st.error(
                    f"Upload failed: "
                    f"{response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI. "
                "Make sure the backend is running."
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )


# =============================
# Question Section
# =============================

st.header("💬 Ask a Question")


question = st.text_area(
    "Your question",
    placeholder=(
        "Example: What is machine learning?"
    ),
    height=120
)


if st.button("🔍 Ask Question"):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "Searching and generating answer..."
            ):

                response = requests.post(
                    f"{API_URL}/query/",
                    params={
                        "question": question
                    },
                    timeout=180
                )

            if response.status_code == 200:

                data = response.json()

                # =====================
                # Answer
                # =====================

                st.header("🤖 Answer")

                st.write(
                    data.get(
                        "answer",
                        "No answer returned."
                    )
                )

                # =====================
                # Groundedness
                # =====================

                st.header("🎯 Groundedness")

                grounded = data.get(
                    "grounded",
                    False
                )

                confidence = data.get(
                    "confidence",
                    0
                )

                if grounded:

                    st.success(
                        f"Grounded ✅ | "
                        f"Confidence: {confidence}"
                    )

                else:

                    st.warning(
                        f"Not fully grounded ⚠️ | "
                        f"Confidence: {confidence}"
                    )

                # =====================
                # Rewritten Query
                # =====================

                rewritten_query = data.get(
                    "rewritten_query",
                    ""
                )

                if rewritten_query:

                    with st.expander(
                        "🔄 Query Rewriting"
                    ):

                        st.write(
                            rewritten_query
                        )

                # =====================
                # Citations
                # =====================

                citations = data.get(
                    "citations",
                    []
                )

                st.header("📚 Sources")

                if citations:

                    for citation in citations:

                        filename = citation.get(
                            "filename",
                            "Unknown"
                        )

                        page = citation.get(
                            "page",
                            "Unknown"
                        )

                        chunk_id = citation.get(
                            "chunk_id",
                            "Unknown"
                        )

                        st.write(
                            f"📄 **{filename}** "
                            f"| Page: {page} "
                            f"| Chunk: {chunk_id}"
                        )

                else:

                    st.write(
                        "No citations available."
                    )

                # =====================
                # Retrieved Context
                # =====================

                retrieved = data.get(
                    "retrieved_chunks",
                    []
                )

                if retrieved:

                    with st.expander(
                        "🔎 Retrieved Context"
                    ):

                        for index, chunk in enumerate(
                            retrieved,
                            start=1
                        ):

                            st.markdown(
                                f"### Chunk {index}"
                            )

                            st.write(
                                chunk.get(
                                    "text",
                                    ""
                                )
                            )

                            st.caption(
                                f"File: "
                                f"{chunk.get('filename', 'Unknown')} "
                                f"| Page: "
                                f"{chunk.get('page', 'Unknown')} "
                                f"| Score: "
                                f"{chunk.get('score', 'N/A')}"
                            )

            else:

                st.error(
                    f"Query failed: "
                    f"{response.text}"
                )

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Cannot connect to FastAPI."
            )

        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )