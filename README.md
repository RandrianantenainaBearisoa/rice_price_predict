# Template ML Engineering
This is my personal template for my Machine learning Engineering projects.
## Goal
My goal with it is to have a reproducible architecture for my futur Machine learning projects.
## Organization
Organized as follow : 
```txt
├── backend 
│   ├── config/                     # Environment & configuration files (YAML/JSON)
│   ├── data/
│   │   ├── data_lake/              # Raw immutable data
│   │   ├── data_warehouse/         # Processed and structured data for EDA
│   │   └── feature_store/          # Model-ready features
│   ├── explorations/               # Notebooks & EDA scripts
│   ├── model/                      # Serialized model artifacts (.joblib, .pkl)
│   ├── pyproject.toml              # Project metadata & dependencies (uv)
│   ├── src/
│   │   ├── api/                    # FastAPI implementation
│   │   │   └── main.py             # API entry point
│   │   └── core/
│   │       ├── pipeline/           # ML Lifecycle scripts
│   │       │   ├── ingestion.py    # Connects to data sources, retrieves raw data, and persists it into the `data_lake`.
│   │       │   ├── cleaning.py     # Handles data validation, missing values, and outliers, moving processed data to the `data_warehouse`.
│   │       │   ├── feat_eng.py     # Transforms data into optimized features (scaling, encoding, selection) and stores them in the `feature_store`.
│   │       │   └── training.py     # Orchestrates model training, hyperparameter tuning, and exports the final artifacts to the `model/` folder.
│   │       └── utils/              # Shared helpers & utilities
│   ├── tests/                      # Unit & Integration test suite
│   └── uv.lock                     # Deterministic dependency lock file
├── LICENSE
├── README.md
└── frontend                        # Minimal vuejs frontend for the test
```

## Requirements
- **Python 3.12+**
- **uv** : Package manager for Python. ([Install uv](https://docs.astral.sh/uv/getting-started/installation/))
- **Node.js (^20.19.0 || >=22.12.0)** & **npm** : For the frontend Vue.js.

## How to use it ?
- Create a new repo based on this template
- Clone the new repo and configure:
```bash
# Clone the new repo
git clone <repo-url>
cd <project-name>

# Backend configuration
cd backend
uv sync # create .venv and install all the dependencies

# Frontend configuration
cd ../frontend
npm install
```
- Exploration data and coding the backend : navigate to the `/backend` folder in the terminal.
    - EDA : ``uv run jupyter notebook`` to run the jupyter notebook server
    - Coding in fastapi: ``uv run uvicorn api.main:app --reload``
- Code the frontend part navigate to the `/frontend` folder in the terminal.
    - ``npm run dev``
