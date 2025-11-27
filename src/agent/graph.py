# graph.py
from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.llm_nodes import llm_answer_node
from agent.ns_nodes import (
    prolog_fact_builder_node,
    consistency_checker_node,
    router_node,
    correction_node,
    response_node,
)


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("llm_answer", llm_answer_node)
    workflow.add_node("build_facts", prolog_fact_builder_node)
    workflow.add_node("check_consistency", consistency_checker_node)
    workflow.add_node("correct", correction_node)
    workflow.add_node("respond", response_node)

    # Entry point
    workflow.set_entry_point("llm_answer")

    # Linear edges
    workflow.add_edge("llm_answer", "build_facts")
    workflow.add_edge("build_facts", "check_consistency")

    # Conditional branch after consistency check
    workflow.add_conditional_edges(
        "check_consistency",
        router_node,
        {
            "needs_correction": "correct",
            "no_correction": "respond",
        },
    )

    workflow.add_edge("correct", "respond")
    workflow.add_edge("respond", END)

    return workflow.compile()
