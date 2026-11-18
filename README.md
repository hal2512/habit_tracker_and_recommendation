# Habit Tracker & Recommendation System

A Streamlit app that logs a student's daily habits, flags days that look like burnout with an unsupervised anomaly detector ("The Guardian"), and suggests specific recovery actions. It also has a rule-based chatbot with voice input and output.

## Features

- **Daily habit logging**: sidebar sliders for sleep, study, social time, screen time, water, exercise, and skipped meals.
- **Anomaly detection**: an Isolation Forest compares the logged day against a healthy baseline and labels it *On Track* or *Irregular Pattern*.
- **Recommendations**: rule-based triggers (sleep < 6 h, social < 0.5 h, study > 9 h, exercise < 15 min) choose tips from a small intervention library (sleep, isolation, overwork, sedentary). If the model flags a day but no rule fires, the app defaults to overwork advice.
- **Guardian chatbot**: keyword-based intent matching (greeting, stress, motivation, sleep, study, stress relief, help). Saying "recommend", "advice", or "fix" makes it call the recommender.
- **Voice**: microphone input through `SpeechRecognition` (Google Web Speech API), with spoken replies from `pyttsx3` (offline TTS).
- **Data analysis page**: compares sleep-hour distributions in the small and the augmented dataset.
- **Model comparison pages**: a model trained on 90 days of data versus one trained on 1,000 days.

## How it works

```
generate_data.py  ──►  data/original_data.csv   (90 days, seed 42)
                  └─►  data/augmented_data.csv  (1,000 days, seed 999)
                               │
train_guardian.py ─────────────┘──►  models/guardian_original.joblib
  (preprocessing.py:                 models/guardian_augmented.joblib
   StandardScaler + IsolationForest)
                               │
app.py (dashboard) ◄───────────┘  + recommender.py (rule-based tips)
pages/1_Chat_with_Guardian.py   ◄── chatbot.py (intents + TTS) + recommender.py
```

1. **Data**: `generate_data.py` simulates daily student logs. Each day has a 5% chance of being a "burnout" day (around 4 h sleep, 10.5 h study, almost no social time or exercise, more screen time, less water, skipped meals). All other days follow a healthy baseline. A `true_label` column (1 = normal, -1 = burnout) is saved for evaluation only. **Both datasets are synthetic.** "Original" is the small set, which stands in for about 3 months of manual logging.
2. **Model**: `preprocessing.py` builds a scikit-learn `Pipeline(StandardScaler → IsolationForest(n_estimators=100, contamination=0.05, random_state=42))`. `train_guardian.py` fits it without labels on 7 features, once per dataset.
3. **Inference**: the dashboard loads `guardian_augmented.joblib`. A prediction of `-1` marks the day as irregular, and `recommender.py` then returns tips based on which rules fired.

## Results

`python evaluate_guardian.py` scores both shipped models against the synthetic `true_label` (positive class = burnout day):

| Model | Evaluated on | Rows | True anomalies | Flagged | Precision | Recall | F1 |
|---|---|---:|---:|---:|---:|---:|---:|
| Original (90 days) | original_data *(training set)* | 90 | 4 | 5 | 0.80 | 1.00 | 0.89 |
| Original (90 days) | augmented_data | 1000 | 46 | 69 | 0.67 | 1.00 | 0.80 |
| Augmented (1,000 days) | original_data | 90 | 4 | 4 | 1.00 | 1.00 | 1.00 |
| Augmented (1,000 days) | augmented_data *(training set)* | 1000 | 46 | 50 | 0.92 | 1.00 | 0.96 |

Caveats: the data comes from one simple generator with well-separated burnout days, so these numbers are a sanity check and do not predict real-world performance. Two rows are scored on the model's own training data. Even so, the model trained on more data flags far fewer false positives (69 → 50 flags on the 1,000-day set).

## Getting started

**Requirements:** Python 3.10+. The voice features also need the PortAudio library for `pyaudio`:
- macOS: `brew install portaudio`
- Debian/Ubuntu: `sudo apt install portaudio19-dev`

```bash
git clone https://github.com/hal2512/habit_tracker_and_recommendation.git
cd habit_tracker_and_recommendation
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

**No API keys or environment variables are needed.** Speech recognition uses the free Google Web Speech endpoint through `SpeechRecognition`, so it needs internet access. Text-to-speech runs locally with `pyttsx3`.

### Regenerating data and models (optional)

The repo ships the small synthetic CSVs (about 40 KB) and the trained models (about 1.9 MB), so the demo runs right after cloning. To rebuild them:

```bash
python generate_data.py     # writes data/*.csv
python train_guardian.py    # writes models/*.joblib
python evaluate_guardian.py # prints the table above
```

The shipped models were pickled with scikit-learn 1.7.2. Newer versions load them with a version warning. If you want to get rid of the warning, retrain with `train_guardian.py`, which gives the same results because the seeds are fixed. Note that `generate_data.py` dates rows relative to today, so regenerated CSVs have different dates but the same values.

## Project structure

```
├── app.py                        # Main dashboard: log a day, detect anomaly, show recommendations
├── pages/
│   ├── 1_Chat_with_Guardian.py   # Text + voice chat with the Guardian bot
│   ├── 2_Data_Analysis.py        # Original vs augmented data distributions
│   ├── 3_Model_Original.py       # Info on the 90-day model
│   └── 4_Model_Augmented.py      # Info on the 1,000-day model
├── chatbot.py                    # Intent matching + pyttsx3 TTS
├── recommender.py                # Rule-based intervention recommender
├── preprocessing.py              # Scaler + Isolation Forest pipeline factory
├── generate_data.py              # Synthetic habit data generator
├── train_guardian.py             # Trains and saves both models
├── evaluate_guardian.py          # Scores models against synthetic labels
├── data/                         # original_data.csv, augmented_data.csv
├── models/                       # Trained pipelines + feature lists (.joblib)
└── requirements.txt
```

## Limitations

- All data is synthetic. Nothing has been tested on real user logs.
- The chat page passes fixed placeholder stats (`sleep_hours=5`, risk = true) to the recommender. It is not yet linked to the dashboard input.
- `pyttsx3` plays audio on the machine running Streamlit, so voice output only works when the app runs locally.

## Tech stack

Python · Streamlit · scikit-learn (Isolation Forest) · pandas · NumPy · Matplotlib · Seaborn · joblib · SpeechRecognition · PyAudio · pyttsx3

---

Originally built as a university project on assistance systems.
