# WildGuard AI - Wildlife Poaching Risk Predictor

WildGuard AI is a Streamlit-based anti-poaching command center for exploring wildlife records and estimating poaching risk.

The application includes a small XGBoost classifier, live species information from Wikipedia, live wildlife occurrence records from GBIF, patrol audit information, and a snare infiltration probability calculator.

## Features

- **Animal Sanctuary Archive**
  - Select protected species such as Asian elephants, Bengal tigers, rhinoceroses, and leopards.
  - Fetch species summaries and photos from Wikipedia.
  - View recent or available global occurrence records from GBIF.
  - Display sightings on an interactive map.

- **Live Threat and Patrol Audit**
  - Review example patrol counteractions by sector.
  - Retrieve live species occurrence records for selected target species.
  - Display occurrence locations on a map.

- **XGBoost Tactical Risk Matrix**
  - Enter time of day, moon phase, road distance, ranger post distance, and animal density.
  - Predict one of three risk levels:
    - Low Risk
    - Average Risk
    - High Risk
  - Receive a plain-language analysis and suggested countermeasures.

- **ML Training and Accuracy Hub**
  - View the XGBoost classifier configuration.
  - Check test accuracy.
  - Analyze feature importance.
  - Compare actual test labels with model predictions.

- **Smart Poacher Trap Calculator**
  - Enter canopy cover, trail usage, and ranger patrol frequency.
  - Estimate snare or trap infiltration probability.
  - Receive a risk level and field countermeasure recommendations.

## Technology Stack

- Python
- Streamlit
- XGBoost
- scikit-learn
- NumPy
- Pandas
- Requests

## External APIs

The application uses:

- **Wikipedia REST API** for species summaries and images.
- **GBIF API** for live wildlife occurrence records and coordinates.

Internet access is required to load live data. If an API is unavailable, the app will display a fallback summary or an empty records table where applicable.

## Installation

### 1. Install Python

Python 3.9 or newer is recommended.

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS or Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install streamlit pandas numpy requests scikit-learn xgboost
```

## Run the Application

From the project folder, run:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, usually:

```text
http://localhost:8501
```

## How the XGBoost Model Works

The classifier is trained on a demonstration dataset containing nine examples and five input features:

1. Time of day
2. Moon phase
3. Distance to the nearest road
4. Distance to the nearest ranger post
5. Endangered animal sightings

The model is split into:

- 67% training data
- 33% test data

Its possible outputs are:

| Value | Risk Level |
|---|---|
| 0 | Low Risk |
| 1 | Average Risk |
| 2 | High Risk |

The test accuracy and feature importance are displayed in the ML Training & Accuracy Hub.

> **Note:** The current training dataset is a small demonstration dataset. The reported accuracy does not represent real-world model performance and should not be used for operational or conservation decisions without validated field data.

## How the Trap Calculator Works

The Smart Poacher Trap Calculator uses the following formula:

```text
Trap probability =
    (canopy cover × 0.4)
  + (footpath usage × 3.5)
  - (patrol frequency × 4.0)
```

The result is limited to a range of 5% to 96%.

- Probability greater than 50%: **HIGH THREAT**
- Probability of 50% or below: **CONTROLLED**

This calculator uses a rule-based formula rather than a trained machine learning model.

## Project Structure

```text
Wildlife Poaching Risk Predictor/
├── app.py
└── README.md
```

## Limitations

- The XGBoost model is trained with a small synthetic dataset.
- Patrol and threat records in the audit module are demonstration data.
- Live GBIF records are not guaranteed to represent poaching incidents.
- Wikipedia and GBIF require internet access.
- The trap probability formula is illustrative and should not replace real field risk assessments.

## Responsible Use

This project is intended for education and decision-support demonstration. It should not be the only basis for safety-critical ranger operations. Real deployments should use validated datasets, professional field verification, and appropriate monitoring safeguards.
