# state.py
from typing import TypedDict, Optional, Dict, Any, List

class AgentState(TypedDict):
    question: str                        # user case description
    llm_raw_answer: Optional[str]
    llm_json: Dict[str, Any]
    prolog_facts: List[str]
    violations: List[str]
    corrected_answer: Dict[str, Any]
    reasoning_trace: List[str]
    final_text_response: Optional[str]