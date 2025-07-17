# FASTAPI Tutorial Code by CampusX (Pydantic Crash Course Included)

This repository contains my practice code for FastAPI, focusing on machine learning model deployment, as taught by CampusX. It also includes a Pydantic crash course.

## What's Inside

This repository provides code examples for:

*   Serving machine learning models using FastAPI.
*   A crash course on Pydantic, a data validation and settings management library.

## Repository Structure

*   `app.py`: Main FastAPI application file for the Patient Management System.
*   `patients.json`: JSON file storing patient data.
*   `pydantic_campusX/`: Contains Pydantic crash course code.
    *   `1_pydantic_why.py`: Examples explaining the purpose of Pydantic.
    *   `2_filed_validation.py`: Code demonstrating field validation in Pydantic.
    *   `3_model_validator.py`: Examples of model validators.
    *   `4_computed_fields.py`: Code showcasing computed fields in Pydantic models.
    *   `5_nested_model.py`: Examples of nested Pydantic models.
    *   `6_serialization.py`: Code related to Pydantic model serialization.
    *   `Readme.md`: Readme file for the Pydantic crash course.
*   `serving_ml_model/`: Contains code for serving ML models with FastAPI.
    *   `backend.py`: Backend implementation for the ML model.
    *   `fastapi_ml_model.ipynb`: Jupyter Notebook demonstrating model training on a dummy data.
    *   `frontend.py`: Frontend code (if any) for interacting with the ML model.
    *   `insurance.csv`: Sample data for the insurance prediction model.
    *   `model.pkl`: Pre-trained machine learning model.

## Patient Management System API Endpoints

The `app.py` file implements a Patient Management System with the following endpoints:

*   `GET /`: Returns a welcome message.
*   `GET /about`: Returns information about the API.
*   `GET /view`: Returns all patient data.
*   `GET /patient/{patient_id}`: Returns data for a specific patient.
*   `GET /sort`: Sorts patients based on height, weight, or BMI.
*   `POST /create`: Creates a new patient.
*   `PUT /edit/{patient_id}`: Updates an existing patient.
*   `DELETE /delete/{patient_id}`: Deletes a patient.

## Pydantic Crash Course

The `pydantic_campusX/` directory contains a set of Python scripts that serve as a crash course on Pydantic. Each file focuses on a specific aspect of Pydantic, such as field validation, model validators, computed fields, nested models, and serialization.

## Serving ML Models

The `serving_ml_model/` directory contains the necessary files to serve machine learning models using FastAPI. The `backend.py` file likely contains the FastAPI application code, while `fastapi_ml_model.ipynb` provides a more detailed, step-by-step example in a Jupyter Notebook.

## Dependencies

*   FastAPI
*   Pydantic
*   Uvicorn (or other ASGI server)

## Setup and Usage

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/GhufranBarcha/fastapi_machine_learning_campusX.git
    cd fastapi_tutorial_project_campusX
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**

    ```bash
    pip install fastapi uvicorn pydantic
    # Install any other dependencies required by the specific ML model serving code
    ```

4.  **Run the Patient Management System:**

    ```bash
    uvicorn app:app --reload
    ```

5.  **Access the API:**

    Open your browser and go to `http://127.0.0.1:8000` (or the address shown in the terminal).

## Notes

*   This repository is intended for educational purposes.
*   The `model.pkl` file is a pre-trained machine learning model. You may need to train your own model or obtain a different pre-trained model depending on your specific use case.
*   Refer to the individual `Readme.md` files in the `pydantic_campusX/` and `serving_ml_model/` directories for more specific instructions and details.