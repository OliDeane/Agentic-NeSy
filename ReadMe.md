# Agentic Neuro-Symbolic Reasoning System

## LLM + Prolog Knowledge Base + LangGraph Agent

This repository implements a neurosymbolic AI agent that combines:
Large Language Models (LLMs) using Gemini via LangChain
Symbolic reasoning using a Prolog knowledge base with logical constraints
Agentic execution using a LangGraph state-machine architecture
to produce logically consistent, correctable, and explainable answers in a simplified medical diagnosis domain.

### IMPORTANT DISCLAIMER:
This project uses a toy medical domain for demonstration only.
It is not medical advice and must not be used for real-world decision-making.


## PROJECT OVERVIEW
Modern LLMs are powerful but often hallucinate or generate answers that violate simple domain rules.
This project solves that problem by combining an LLM with a symbolic knowledge base (KB) that enforces strict logical constraints.

### Pipeline Summary:

- User provides a case description in natural language.
- The LLM generates a structured JSON answer (diagnosis, treatments, symptoms).
- The JSON is converted into Prolog facts for a specific patient instance.
- Prolog evaluates the facts under its rule base and checks for violations.

- If violations exist, a correction loop is triggered:
- The LLM receives the violations and the rules
- The LLM produces a corrected JSON answer that satisfies KB constraints
- The agent returns the final answer along with a reasoning trace showing each step.


## IMPORTANT FILES

- kb.pl - Prolog knowledge base (facts and constraints)
- state.py - AgentState definition used by LangGraph
- llm_nodes.py - LLM-related nodes (Gemini answer, correction)
- ns_nodes.py - Neurosymbolic nodes (Prolog interface, consistency checking, response)
- prolog_interface.py - Python-to-Prolog bridge functions using pyswip
- graph.py - LangGraph workflow definition
- run_demo.py - Command-line demo for running the agent

## KEY COMPONENTS

### Prolog Knowledge Base
The file kb.pl defines a toy medical domain consisting of diseases, symptoms, drug classes, and rules.
It includes logic for identifying violations such as:
- missing required symptoms
- contraindicated medications
- incompatible diagnosis-symptom patterns

### LLM Structured Output
The agent prompts a Gemini model (gemini-2.5-flash) to return strictly formatted JSON with keys:
- diagnosis
- explanation
- recommended_treatments
- evidence_symptoms
- Consistency Checking

The LLM output is converted to Prolog facts.
Prolog then checks whether these facts violate any logical rules using the violation/1 predicate.

### Correction Loop
If violations are found, the LLM is prompted again with:
the original JSON answer
the list of formula violations
natural language descriptions of the rules
The LLM returns a corrected JSON answer that satisfies the KB constraints.

### LangGraph Agent
The system is implemented as a LangGraph state machine:
LLM Answer
     ↓
Build Prolog Facts
     ↓
Check Constraints
     ↓
If violations exist → Correction
     ↓
Response

LangGraph handles state propagation, node execution, and branching.

## INSTALLATION

Create a virtual environment:
```python
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:
```python
pip install -r requirements.txt
```

Add your Google API key to a .env file:
GOOGLE_API_KEY=your_key_here

### RUNNING THE DEMO
Run the main agent pipeline. Navigate to the src directory and run:
python main.py

### Example output:

=== Final Answer ===
Diagnosis: common_cold
Recommended treatments: ['paracetamol']
Explanation:
Because the patient displays symptoms associated with common cold...
Corrected by KB/LLM: True
=== Reasoning Trace ===
LLM produced initial JSON answer.
Asserted Prolog facts: [...]
Detected violation: contraindicated_drug(p1, influenza, nsaid, ibuprofen)
Applied LLM-based correction using constraints.
