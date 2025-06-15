import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Salary Advance & Loan Calculator", layout="centered")

# App title and intro
st.title(" Salary Advance💵 & Loan Calculator💳 ")
st.markdown("Easily estimate your advance eligibility or loan payment plan.")

# Collect user name
name = st.text_input("👤 Enter your name")

# Radio option: choose between salary advance or loan
option = st.radio("What would you like to calculate?", ["💵 Salary Advance", "📊 Loan Calculator"])
st.markdown("---")

# === Salary Advance Section ===
if option == "💵 Salary Advance":
    st.subheader("Salary Advance Details")

    gross_salary = st.number_input("Gross Salary", min_value=0.0, format="%.2f")
    pay_frequency = st.selectbox("Pay Frequency", ["monthly", "weekly", "biweekly"])
    requested_amount = st.number_input("Requested Advance Amount", min_value=0.0, format="%.2f")

    if st.button("🧮 Calculate Advance"):
            try:
                res = requests.post("http://backend:8000/calculate_advance", json={
                    "gross_salary": gross_salary,
                    "pay_frequency": pay_frequency,
                    "requested_amount": requested_amount
                })
                output = res.json()

                if output["eligible"]:
                    st.success("✅ You are eligible for this advance.")
                else:
                    st.error("❌ You are not eligible for the requested amount.")

                st.write(f"**Employee name:{name}**")
                st.write(f"**Requested Amount:** ${output['requested']:.2f}")
                st.write(f"**Maximum Eligible Amount:** ${output['max_eligible_amount']:.2f}")
                st.write(f"**Fee (5%):** ${output['fee']:.2f}")
                st.write(f"**Total Due:** ${output['total_due']:.2f}")

            except Exception as e:
                st.error("⚠️ Error processing your request.")
                st.write(e)

# === Loan Calculator Section ===
elif option == "📊 Loan Calculator":
    st.subheader("Loan Calculator Details")

    principal = st.number_input("Loan Amount", min_value=0.0, format="%.2f")
    rate = st.number_input("Annual Interest Rate (%)", min_value=0.0, format="%.2f")
    years = st.number_input("Loan Term (Years)", min_value=1)

    if st.button("🧮 Calculate Loan"):
        try:
            res = requests.post("http://backend:8000/calculate_loan", json={
                "principal": principal,
                "annual_rate": rate,
                "years": years
            })
            output = res.json()

            st.success(f"Loan Calculation for {name if name else 'User'}")
            st.write(f"💰 **Monthly Payment:** ${output['monthly_payment']}")
            st.write(f"📈 **Total Payment:** ${output['total_payment']}")
            
        except Exception as e:
            st.error("Error processing your request.")
            st.write(e)
