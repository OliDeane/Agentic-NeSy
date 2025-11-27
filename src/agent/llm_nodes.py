# llm_nodes.py
import json
from typing import Any, Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from agent.state import AgentState

# This is the LLM you tested
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
)


def llm_answer_node(state: AgentState) -> AgentState:
    question = state["question"]

    prompt = f"""
You are a medical assistant working in a toy domain with a small set
of diseases and symptoms. This is ONLY for demonstration; do not give
real-world medical advice.

Given the following case description, respond ONLY with a JSON object
with keys:
- diagnosis (string)
- explanation (string)
- recommended_treatments (array of strings)
- evidence_symptoms (array of strings)

Case:
{question}

Example format:
{{
  "diagnosis": "influenza",
  "explanation": "Because the patient has fever and cough...",
  "recommended_treatments": ["paracetamol"],
  "evidence_symptoms": ["fever", "cough"]
}}
"""

    # Use the same pattern you tested:
    # llm.invoke("...").content
    msg = llm.invoke(prompt)
    text = msg.content if isinstance(msg.content, str) else str(msg.content)
    text = text.strip()

    try:
        data: Dict[str, Any] = json.loads(text)
    except json.JSONDecodeError:
        # very naive fallback; improve later if you like
        data = {"raw": text}

    state["llm_raw_answer"] = text
    state["llm_json"] = data
    state["reasoning_trace"].append("LLM produced initial JSON answer.")
    return state
