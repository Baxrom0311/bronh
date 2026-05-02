# Respiratory NB Explainability

- Model type: categorical_naive_bayes
- Model version: 1
- Samples: 162
- Labels: 7
- Features: 18

## Global Top Signals

| Label | Feature | Value | Support score | Lift | Count |
| --- | --- | --- | ---: | ---: | ---: |
| ARVI / oddiy shamollash | runny_nose | yes | 4.883 | 132.0 | 21 |
| COVID-19 (mumkin) | loss_of_taste | yes | 4.863 | 129.414 | 26 |
| COVID-19 (mumkin) | covid_contact | yes | 4.863 | 129.414 | 26 |
| Shoshilinch yordam kerak | oxygen_bin | critical | 4.816 | 123.519 | 22 |
| Shoshilinch yordam kerak | heart_rate_bin | very_high | 4.772 | 118.148 | 21 |

## ARVI / oddiy shamollash

- Sample count: 21
- Prior probability: 0.13

| Feature | Value | Support score | Lift | Count |
| --- | --- | ---: | ---: | ---: |
| runny_nose | yes | 4.883 | 132.0 | 21 |
| fatigue_bin | none | 3.517 | 33.692 | 5 |
| heart_rate_bin | normal | 2.978 | 19.654 | 20 |
| fatigue_bin | mild | 2.161 | 8.678 | 16 |
| oxygen_bin | normal | 1.926 | 6.863 | 21 |

## Astma xuruji

- Sample count: 22
- Prior probability: 0.136

| Feature | Value | Support score | Lift | Count |
| --- | --- | ---: | ---: | ---: |
| chronic_bucket | asthma | 3.461 | 31.846 | 22 |
| temperature_bin | normal | 1.772 | 5.882 | 22 |
| cough_type | none | 1.745 | 5.728 | 15 |
| oxygen_bin | low | 1.558 | 4.751 | 22 |
| heart_rate_bin | high | 1.199 | 3.317 | 20 |

## Bronxit

- Sample count: 24
- Prior probability: 0.148

| Feature | Value | Support score | Lift | Count |
| --- | --- | ---: | ---: | ---: |
| chronic_bucket | copd | 1.98 | 7.245 | 9 |
| duration_bin | long | 1.778 | 5.917 | 6 |
| smoker | yes | 1.758 | 5.802 | 19 |
| oxygen_bin | borderline | 1.349 | 3.852 | 24 |
| temperature_bin | mild | 1.288 | 3.626 | 24 |

## COVID-19 (mumkin)

- Sample count: 26
- Prior probability: 0.16

| Feature | Value | Support score | Lift | Count |
| --- | --- | ---: | ---: | ---: |
| loss_of_taste | yes | 4.863 | 129.414 | 26 |
| covid_contact | yes | 4.863 | 129.414 | 26 |
| diarrhea | yes | 3.647 | 38.345 | 7 |
| temperature_bin | mild | 1.276 | 3.584 | 25 |
| cough_type | dry | 1.122 | 3.07 | 26 |

## Gripp

- Sample count: 22
- Prior probability: 0.136

| Feature | Value | Support score | Lift | Count |
| --- | --- | ---: | ---: | ---: |
| headache_level | severe | 1.835 | 6.265 | 6 |
| sore_throat | yes | 1.358 | 3.89 | 16 |
| temperature_bin | high | 1.16 | 3.189 | 18 |
| cough_type | dry | 1.032 | 2.807 | 22 |
| dyspnea_level | none | 0.95 | 2.586 | 12 |

## Shoshilinch yordam kerak

- Sample count: 22
- Prior probability: 0.136

| Feature | Value | Support score | Lift | Count |
| --- | --- | ---: | ---: | ---: |
| oxygen_bin | critical | 4.816 | 123.519 | 22 |
| heart_rate_bin | very_high | 4.772 | 118.148 | 21 |
| respiratory_rate_bin | critical | 4.571 | 96.667 | 17 |
| temperature_bin | very_high | 4.389 | 80.556 | 14 |
| cough_type | bloody | 4.166 | 64.444 | 11 |

## Zotiljam (pnevmoniya)

- Sample count: 25
- Prior probability: 0.154

| Feature | Value | Support score | Lift | Count |
| --- | --- | ---: | ---: | ---: |
| oxygen_bin | low | 1.677 | 5.351 | 25 |
| temperature_bin | high | 1.594 | 4.923 | 25 |
| respiratory_rate_bin | high | 1.555 | 4.733 | 16 |
| duration_bin | long | 1.427 | 4.167 | 5 |
| cough_type | wet | 1.316 | 3.729 | 25 |
