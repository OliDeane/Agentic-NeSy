% kb.pl
% ---------------------------
% Toy medical KB (DO NOT use in real life)

:- dynamic patient/1.
:- dynamic diagnosis/2.
:- dynamic observed_symptom/2.
:- dynamic recommended_treatment/2.


% Diseases
disease(influenza).
disease(common_cold).
disease(asthma).

% Symptoms
symptom(fever).
symptom(cough).
symptom(runny_nose).
symptom(shortness_of_breath).

% Typical disease-symptom associations
has_symptom(influenza, fever).
has_symptom(influenza, cough).
has_symptom(common_cold, runny_nose).
has_symptom(common_cold, cough).
has_symptom(asthma, shortness_of_breath).

% Drug classes / examples
drug_class(ibuprofen, nsaid).
drug_class(paracetamol, analgesic).

% Disease-level contraindications (disease, drug_class)
contraindicated(asthma, nsaid).

% Runtime facts will be asserted like:
  patient(p1).
  diagnosis(p1, influenza).
  observed_symptom(p1, fever).
  observed_symptom(p1, cough).
  recommended_treatment(p1, ibuprofen).

% --------- Constraints as violations ---------

% Missing required symptom:
% If diagnosis(P, D) and D usually has symptom S, but S not observed for P.
violation(missing_required_symptom(P, D, S)) :-
    diagnosis(P, D),
    has_symptom(D, S),
    \+ observed_symptom(P, S).

% Contraindicated drug:
% If diagnosis(P, D) and recommended drug has a class that is contraindicated.
violation(contraindicated_drug(P, D, DrugClass, Drug)) :-
    diagnosis(P, D),
    recommended_treatment(P, Drug),
    drug_class(Drug, DrugClass),
    contraindicated(D, DrugClass).

% Candidate alternative diagnoses:
% All observed symptoms for P are symptoms of D.
candidate_diagnosis(P, D) :-
    disease(D),
    patient(P),
    forall(observed_symptom(P, S), has_symptom(D, S)).
