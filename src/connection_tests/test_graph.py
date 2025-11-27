from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

class AgentState(TypedDict):
    question : str
    draft_answer : Optional[str]
    final_answer : Optional[str]
    requires_elaboration : bool

def draft_answer(state:AgentState) -> AgentState:
    question = state["question"]
    state["draft_answer"] = f"This is the initial answer to the question: {question}"
    return state

def check_answer(state:AgentState) -> AgentState:

    if "complete" not in state["draft_answer"]: 
        state["requires_elaboration"] = True
    else:
        state["requires_elaboration"] = False
    
    return state

def passthrough(state:AgentState) -> AgentState:
    state["final_answer"] = state["draft_answer"]
    
    return state

def elaborate(state:AgentState) -> AgentState:
    state["final_answer"] = state["draft_answer"] + " complete!"
    return state

def router_node(state:AgentState) -> AgentState:
    if state["requires_elaboration"]:
        return "elaborate"
    else:
        return "passthrough"

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("draft", draft_answer)
    workflow.add_node("check", check_answer)
    workflow.add_node("passthrough", passthrough)
    workflow.add_node("elaborate", elaborate)
    # workflow.add_node("router",router_node)

    workflow.set_entry_point("draft")

    workflow.add_edge("draft","check")

    workflow.add_conditional_edges(
        "check",
        router_node,
        {"passthrough":"passthrough", 
         "elaborate":"elaborate"}
    )

    workflow.add_edge("passthrough",END)
    workflow.add_edge("elaborate",END)

    return workflow.compile()

if __name__ == "__main__":
    graph = build_graph()
    initial_state: AgentState = {
        "question": "What are you?",
        "draft_answer": None,
        "final_answer": None,
        "requires_elaboration": False   
    }
    output = graph.invoke(initial_state)
    print(output)
