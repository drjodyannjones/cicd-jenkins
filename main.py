from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from prediction_model.predict import generate_predictions
import logging

app = FastAPI(
    title="Loan Prediction App using API - CI CD Jenkins",
    description="A Simple CI CD Demo",
    version="1.0",
)

# Configuring basic logger
logging.basicConfig(level=logging.INFO)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class LoanPrediction(BaseModel):
    Gender: str
    Married: str
    Dependents: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str


@app.get("/")
def index():
    return {"message": "Welcome to Loan Prediction App using API - CI CD Jenkins"}


@app.post("/prediction_status")
def predict(loan_details: LoanPrediction):
    return perform_prediction(loan_details)


@app.post("/prediction_ui")
def predict_gui(loan_details: LoanPrediction):
    return perform_prediction(loan_details)


def perform_prediction(loan_details: LoanPrediction):
    try:
        data = loan_details.dict()
        prediction_result = generate_predictions([data])
        prediction = prediction_result.get("prediction", [None])[0]
        if prediction is None:
            raise ValueError("Prediction function did not return a valid response.")
        pred = "Approved" if prediction == "Y" else "Rejected"
        return {"status": pred}
    except ValueError as e:
        logging.error(f"Error during prediction: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8005)
