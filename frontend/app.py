import streamlit as st
import pandas as pd
import requests

st.title("Salary Advance💵 & Loan Calculator 💳")
name = st.text_input("Enter your name")

option = st.radio("Choose an option:", ["Salary Advance", "Loan Calculator"])

if option == "Salary Advance":
    gross_salary = st.number_input("Gross Salary", min_value=0.0)
    pay_frequency = st.selectbox("Pay Frequency", ["monthly", "weekly", "biweekly"])
    # No limit needed on the amount requested.
    requested_amount = st.number_input("Requested Advance Amount", min_value=0.0)

    if st.button("Calculate Advance"):
        res = requests.post("http://backend:8000/calculate_advance", json={
            "gross_salary": gross_salary,
            "pay_frequency": pay_frequency,
            "requested_amount": requested_amount
        })
        st.json(res.json())

elif option == "Loan Calculator":
    principal = st.number_input("Loan Amount", min_value=0.0)
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0)
    years = st.number_input("Loan Term (Years)", min_value=1)

    if st.button("Calculate Loan"):
        res = requests.post("http://backend:8000/calculate_loan", json={
            "principal": principal,
            "annual_rate": rate,
            "years": years
        })
        output = res.json()
        st.write(f"Employe name{name}")
        st.write(f"Monthly Payment: ${output['monthly_payment']}")
        st.write(f"Total Payment: ${output['total_payment']}")
        st.write("Amortisation Schedule:")
        df = pd.DataFrame(output['schedule'])
        st.dataframe(df)