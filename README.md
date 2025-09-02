This repo contains code from CampusX GenAI related tutorials.

## 1. FastAPI CampusX
FastAPI + ML serving examples:
- Basic CRUD & patients example (`app.py`, `patients.json`).
- Packaged ML serving demo (zip + `serving_ml_model/` with `backend.py`, `frontend.py`, `model.pkl`).
- Insurance premium prediction microservice (`insurance-premium-prediction-fastapi/`): Pydantic schemas, model loading (`model/predict.py`), config (`config/city_tier.py`), FastAPI app (`app.py`).

## 2. Pydantic CampusX
Focused scripts showing core Pydantic features:
- Why / introduction (`1_pydantic_why.py`).
- Field validation & constraints (`2_filed_validation.py`).
- Model validators (`3_model_validator.py`).
- Computed fields (`4_computed_fields.py`).
- Nested models (`5_nested_model.py`).
- Serialization & export (`6_serialization.py`).

## 3. LangGraph CampusX
LangGraph + LLM workflow notebooks & mini apps:
- Step‑by‑step notebooks: installation, simple LLM flow, prompt chaining, task workflows (BMI, batsman stats, essay, quadratic solver, review reply, X post generator, basic chatbot, persistence).
- Chatbot demo suites (`11_langgraph_chatbots/`): basic chatbot, streaming responses, resume chatbot, SQLite + persistence example (backend + Streamlit frontends).

## 4. LangSmith CampusX
Demonstrates LangChain and LangSmith for building and monitoring LLM applications:
- Simple and sequential LLM chains (`1_simple_llm_call.py`, `2_sequential_chain.py`).
- RAG pipeline implementations (`3_rag_v*.py`).
- ReAct agent with custom tools (`4_agent.py`).
- LangGraph workflow for essay evaluation (`5_langgraph.py`).

---
Lightweight, self‑contained examples; open each folder for details.
