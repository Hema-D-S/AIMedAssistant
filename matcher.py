# evaluate_matcher.py

import pandas as pd
from brain_of_the_doctor.matcher import SymptomMatcher
from sklearn.metrics import precision_score, recall_score, f1_score, classification_report

# Load your matcher with the real symptom-disease dataset
matcher = SymptomMatcher("dataset1.csv")

# Load test cases with ground truth
df = pd.read_csv("test_cases.csv")

y_true = []
y_pred = []

for _, row in df.iterrows():
    true_disease = row["Expected Disease"]
    text = row["Voice Transcription"]

    symptoms = matcher.extract_symptoms(text)
    matches = matcher.match_symptoms_to_diseases(symptoms)

    if matches:
        predicted_disease = matches[0][0]
    else:
        predicted_disease = "none"

    y_true.append(true_disease.lower())
    y_pred.append(predicted_disease.lower())

# Print precision, recall, F1-score
print("✅ Evaluation Results:")
print(classification_report(y_true, y_pred))
