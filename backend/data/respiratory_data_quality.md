# Respiratory Dataset Quality Report

- Dataset path: `data/respiratory_canonical_dataset.csv`
- Total rows: `203`
- Duplicate rows: `5`
- Duplicate rate: `0.025`
- Class balance ratio: `1.0`

## Warnings
- 5 ta takrorlangan qator aniqlandi.
- Missing qiymatlar bor: chronic_diseases.

## Recommendations
- Deduplication bosqichini cleaning pipeline ga qo'shing.
- Missing qiymatlar uchun imputatsiya yoki exclusion qoidalarini yozing.

## Missing Counts
- temperature: 0
- cough_type: 0
- dyspnea_level: 0
- sore_throat: 0
- runny_nose: 0
- headache_level: 0
- muscle_pain: 0
- fatigue_level: 0
- duration_days: 0
- oxygen_saturation: 0
- heart_rate: 0
- respiratory_rate: 0
- chest_pain: 0
- loss_of_taste: 0
- diarrhea: 0
- covid_contact: 0
- smoker: 0
- chronic_diseases: 154
- diagnosis_label: 0

## Out Of Range Counts
- temperature: 0
- fatigue_level: 0
- duration_days: 0
- oxygen_saturation: 0
- heart_rate: 0
- respiratory_rate: 0
