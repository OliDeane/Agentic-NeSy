# prolog_interface.py
from typing import List
from pyswip import Prolog

PATIENT_ID = "p1"  # fixed for single-case runs
prolog = Prolog()
prolog.consult("symbolic/kb.pl")


def prolog_atom(s: str) -> str:
    """
    Turn an arbitrary string into a Prolog-safe atom.
    Very simple: lowercase, replace spaces with underscores.
    You can improve this if needed.
    """
    return s.strip().lower().replace(" ", "_")


def reset_patient_facts():
    # Retract any previous patient-specific facts.
    list(prolog.query(f"retractall(patient({PATIENT_ID}))."))
    list(prolog.query(f"retractall(diagnosis({PATIENT_ID}, _))."))
    list(prolog.query(f"retractall(observed_symptom({PATIENT_ID}, _))."))
    list(prolog.query(f"retractall(recommended_treatment({PATIENT_ID}, _))."))


def assert_fact(fact_str: str):
    """
    fact_str: e.g. 'patient(p1).' or 'diagnosis(p1, influenza).'
    """
    list(prolog.query(f"assertz({fact_str})."))


def build_patient_facts_from_json(j: dict) -> List[str]:
    diagnosis = j.get("diagnosis")
    symptoms = j.get("evidence_symptoms", []) or []
    treatments = j.get("recommended_treatments", []) or []

    facts: List[str] = [f"patient({PATIENT_ID})"]

    if diagnosis:
        facts.append(f"diagnosis({PATIENT_ID}, {prolog_atom(diagnosis)})")

    for s in symptoms:
        facts.append(f"observed_symptom({PATIENT_ID}, {prolog_atom(s)})")

    for t in treatments:
        facts.append(f"recommended_treatment({PATIENT_ID}, {prolog_atom(t)})")

    return facts


def query_violations() -> List[str]:
    violations: List[str] = []
    for sol in prolog.query("violation(V)."):
        violations.append(str(sol["V"]))
    return violations


def query_candidate_diagnoses() -> List[str]:
    cands: List[str] = []
    for sol in prolog.query(f"candidate_diagnosis({PATIENT_ID}, D)."):
        cands.append(str(sol["D"]))
    return cands
