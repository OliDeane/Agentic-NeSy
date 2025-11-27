# run_demo.py
from state import AgentState
from graph import build_graph

def main():
    graph = build_graph()

    question = (
        "Patient has cough and runny nose, no asthma history. "
        "What is the likely diagnosis and treatment?"
    )

    initial_state: AgentState = {
        "question": question,
        "llm_raw_answer": None,
        "llm_json": {},
        "prolog_facts": [],
        "violations": [],
        "corrected_answer": {},
        "reasoning_trace": [],
        "final_text_response": None,
    }

    final_state = graph.invoke(initial_state)
    print(final_state["final_text_response"])

if __name__ == "__main__":
    main()
