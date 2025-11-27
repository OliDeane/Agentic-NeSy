from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    question: str
    draft_answer: Optional[str]
    final_answer: Optional[str]
    needs_elaboration: bool

# Node 1 - call the LLM (fake for now)
def draft_answer_node(state: AgentState) -> AgentState:
    question = state["question"]
    # pretend this is an LLM call – replace with real API later
    state["draft_answer"] = f"Short answer to: {question}"
    return state

# Node 2: check if answer is too short
def check_answer_length_node(state: AgentState) -> AgentState:
    ans = state["draft_answer"] or ""
    state["needs_elaboration"] = len(ans.split()) < 10
    return state

# Node 3: ask LLM to elaborate if needed
def elaborate_answer_node(state: AgentState) -> AgentState:
    draft = state["draft_answer"] or ""
    # again, pretend LLM – realistically you'd prompt: "expand this answer"
    state["final_answer"] = draft + " ...and here is some more detailed explanation."
    return state

# Node 4: Pass-through when no elaboration required
def passthrough_node(state: AgentState) -> AgentState:
    state["final_answer"] = state["draft_answer"]
    return state

# Decide whether to elaborate or not
def router_node(state: AgentState) -> str:
    return "elaborate" if state["needs_elaboration"] else "passthrough"

# Wire it together with LangGraph
def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("draft", draft_answer_node)
    workflow.add_node("check_length", check_answer_length_node)
    workflow.add_node("elaborate", elaborate_answer_node)
    workflow.add_node("passthrough", passthrough_node)

    # Entry
    workflow.set_entry_point("draft")

    # Flow: draft -> check_length
    workflow.add_edge("draft", "check_length")

    # Conditional: from check_length, go to elaborate OR passthrough
    workflow.add_conditional_edges(
        "check_length",
        router_node,
        {
            "elaborate": "elaborate",
            "passthrough": "passthrough",
        },
    )

    # Both branches then end
    workflow.add_edge("elaborate", END)
    workflow.add_edge("passthrough", END)

    return workflow.compile()

if __name__ == "__main__":
    graph = build_graph()
    initial_state: AgentState = {
        "question": "What is neurosymbolic AI?",
        "draft_answer": None,
        "final_answer": None,
        "needs_elaboration": False,
    }
    final_state = graph.invoke(initial_state)
    print(final_state["final_answer"])
