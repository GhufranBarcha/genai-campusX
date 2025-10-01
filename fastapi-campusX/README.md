# FastAPI CampusX

Concise examples for FastAPI + ML serving.

Contents:
- app.py: Patient management API (CRUD, sort, filter).
- patients.json: Sample patient dataset.
- serving_ml_model/: Simple ML model serve demo (backend, frontend, notebook, model.pkl, insurance.csv).
- insurance-premium-prediction-fastapi/: Microservice
  - app.py: Prediction API.
  - model/: model.pkl + predict.py loader.
  - schema/: Pydantic request/response models.
  - config/: city_tier mapping.
  - requirements.txt: Service deps.

Run patient API:
uvicorn app:app --reload

Run insurance service (inside its folder):
uvicorn app:app --reload

Open docs at /docs for interactive schema.

Educational reference; minimal setup required.