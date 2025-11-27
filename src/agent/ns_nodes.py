# ns_nodes.py (top of file)
import json
from typing import List, Dict, Any

from langchain_google_genai import ChatGoogleGenerativeAI

from agent.state import AgentState
from symbolic.prolog_interface import (
    reset_patient_facts,
    build_patient_facts_from_json,
    assert_fact,
    query_violations,
    query_candidate_diagnoses,
)

# You can reuse the same settings, or make this slightly more "creative"
correction_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)

def prolog_fact_builder_node(state: AgentState) -> AgentState:
    reset_patient_facts()
    j: Dict[str, Any] = state["llm_json"]

    facts = build_patient_facts_from_json(j)
    for f in facts:
        assert_fact(f)  # add period for Prolog
    state["prolog_facts"] = facts
    state["reasoning_trace"].append(f"Asserted Prolog facts: {facts}")
    return state


def consistency_checker_node(state: AgentState) -> AgentState:
    violations: List[str] = query_violations()
    state["violations"] = violations

    if violations:
        for v in violations:
            state["reasoning_trace"].append(f"Detected violation: {v}")
    else:
        state["reasoning_trace"].append("No violations detected by Prolog KB.")

    return state


def router_node(state: AgentState) -> str:
    """
    LangGraph will call this to decide where to go next.
    """
    if state["violations"]:
        return "needs_correction"
    return "no_correction"

# ns_nodes.py (continued)

def correction_node(state: AgentState) -> AgentState:
    violations = state["violations"]
    llm_json = state["llm_json"]

    prompt = f"""
The following proposed medical answer JSON violates some logical constraints
from a knowledge base. This is a toy example, not real medical advice.

Original JSON:
{json.dumps(llm_json, indent=2)}

Logical violations (Prolog terms):
{violations}

Natural language rules:
- If a disease usually has a symptom, the patient should have that symptom.
- For patients with asthma, NSAIDs (drug_class: nsaid) are contraindicated.

Please revise the JSON so that it no longer violates these rules while staying
as close as possible to the original intent. Respond ONLY with JSON in the
same format: diagnosis, explanation, recommended_treatments, evidence_symptoms.
"""

    msg = correction_llm.invoke(prompt)
    text = msg.content if isinstance(msg.content, str) else str(msg.content)
    text = text.strip()

    try:
        corrected = json.loads(text)
    except json.JSONDecodeError:
        corrected = {"raw": text}

    state["corrected_answer"] = corrected
    state["reasoning_trace"].append("Applied LLM-based correction using constraints.")
    return state

def response_node(state: AgentState) -> AgentState:
    if state.get("corrected_answer"):
        final = state["corrected_answer"]
        corrected = True
    else:
        final = state["llm_json"]
        corrected = False

    diag = final.get("diagnosis")
    treatments = final.get("recommended_treatments")
    expl = final.get("explanation")

    lines = [
        "=== Final Answer ===",
        f"Diagnosis: {diag}",
        f"Recommended treatments: {treatments}",
        "",
        "Explanation:",
        expl or "",
        "",
        f"Corrected by KB/LLM: {corrected}",
        "",
        "=== Reasoning Trace ===",
        *state.get("reasoning_trace", []),
    ]

    state["final_text_response"] = "\n".join(lines)
    return state