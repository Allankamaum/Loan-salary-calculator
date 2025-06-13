from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

# --- Input Models ---
class AdvanceRequest(BaseModel):
    gross_salary: float
    pay_frequency: str
    requested_amount: float

class LoanRequest(BaseModel):
    principal: float
    annual_rate: float
    years: int

# --- Salary Advance Endpoint ---
@app.post("/calculate_advance")
def calculate_advance(data: AdvanceRequest):
    if data.pay_frequency.lower() == "monthly":
        factor = 1
    elif data.pay_frequency.lower() == "biweekly":
        factor = 2
    elif data.pay_frequency.lower() == "weekly":
        factor = 4
    else:
        factor = 1  # default to monthly

    max_allowed = (data.gross_salary / factor) * 0.5
    is_eligible = data.requested_amount <= max_allowed

    if is_eligible:
        fee = data.requested_amount * 0.05
    else:
        fee = 0.0

    total_due = data.requested_amount + fee

    return {
        "eligible": is_eligible,
        "requested": data.requested_amount,
        "max_eligible_amount": round(max_allowed, 2),
        "fee": round(fee, 2),
        "total_due": round(total_due, 2)
    }

# --- Loan Calculator Endpoint ---
@app.post("/calculate_loan")
def calculate_loan(data: LoanRequest):
    total_months = data.years * 12
    monthly_rate = data.annual_rate / 100 / 12

    if monthly_rate == 0:
        monthly_payment = data.principal / total_months
    else:
        x = (1 + monthly_rate) ** total_months
        monthly_payment = data.principal * monthly_rate * x / (x - 1)

    remaining = data.principal
    schedule = []

    for month in range(1, total_months + 1):
        interest = remaining * monthly_rate
        principal_paid = monthly_payment - interest
        remaining -= principal_paid
        schedule.append({
            "Month": month,
            "Principal": round(principal_paid, 2),
            "Interest": round(interest, 2),
            "Balance": round(max(remaining, 0), 2)
        })

    return {
        "monthly_payment": round(monthly_payment, 2),
        "total_payment": round(monthly_payment * total_months, 2),
        "schedule": pd.DataFrame(schedule).to_dict(orient="records")
    }

