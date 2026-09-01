from langgraph.graph import (
    StateGraph,
    START,
    END
)

from app.graph.state import RAGState

from app.graph.nodes import (
    rewrite_node,
    retrieve_node,
    rerank_node,
    generate_node,
    groundedness_node
)


def build_workflow():

    graph = StateGraph(RAGState)

    graph.add_node(
        "rewrite",
        rewrite_node
    )

    graph.add_node(
        "retrieve",
        retrieve_node
    )

    graph.add_node(
        "rerank",
        rerank_node
    )

    graph.add_node(
        "generate",
        generate_node
    )

    graph.add_node(
        "groundedness",
        groundedness_node
    )

    graph.add_edge(
        START,
        "rewrite"
    )

    graph.add_edge(
        "rewrite",
        "retrieve"
    )

    graph.add_edge(
        "retrieve",
        "rerank"
    )

    graph.add_edge(
        "rerank",
        "generate"
    )

    graph.add_edge(
        "generate",
        "groundedness"
    )

    graph.add_edge(
        "groundedness",
        END
    )

    return graph.compile()