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

% Drug classes and examples
drug_class(ibuprofen, nsaid).
drug_class(paracetamol, analgesic).

% Contraindications
contraindicated(asthma, nsaid).

% Runtime facts (per patient) will be asserted like:
%   patient(p1).
%   diagnosis(p1, influenza).
%   observed_symptom(p1, fever).
%   recommended_treatment(p1, ibuprofen).

% --- Constraints as violations ---

% 1) Missing required symptom
violation(missing_required_symptom(P, D, S)) :-
    diagnosis(P, D),
    has_symptom(D, S),
    \+ observed_symptom(P, S).

% 2) Contraindicated drug
violation(contraindicated_drug(P, D, DrugClass, Drug)) :-
    diagnosis(P, D),
    recommended_treatment(P, Drug),
    drug_class(Drug, DrugClass),
    contraindicated(D, DrugClass).
