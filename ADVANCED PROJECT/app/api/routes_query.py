from fastapi import APIRouter, HTTPException

from app.graph.workflow import build_workflow


router = APIRouter(
    prefix="/query",
    tags=["Query"]
)


# Build LangGraph workflow
rag_workflow = build_workflow()


@router.post("/")
def query_document(question: str):

    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = rag_workflow.invoke({
            "question": question
        })

        return {
            "success": True,
            "question": question,
            "rewritten_query": result.get(
                "rewritten_query",
                ""
            ),
            "retrieved_chunks": result.get(
                "retrieved_chunks",
                []
            ),
            "reranked_chunks": result.get(
                "reranked_chunks",
                []
            ),
            "answer": result.get(
                "answer",
                ""
            ),
            "grounded": result.get(
                "grounded",
                False
            ),
            "confidence": result.get(
                "confidence",
                0.0
            ),
            "citations": result.get(
                "citations",
                []
            )
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )