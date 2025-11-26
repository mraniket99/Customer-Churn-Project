import streamlit as st
import requests

#fastapi endpoint
API_URL = 'http://127.0.0.1:8000/predict'

st.title("Customer Churn Prediction APP")

st.write("Fill the following details and get the churn prediction of that customer")

# Numeric Inputs
session_duration = st.number_input("Session Duration", min_value=0.0)
avg_order_value = st.number_input("Average Order Value", min_value=0.0)
customer_service_calls= st.number_input("Customer Service Calls", min_value = 0.0)
app_transactions = st.number_input("App Transactions", min_value = 0.0)
desktop_sessions = st.number_input("Desktop Session", min_value = 0.0)
product_detail_view_per_app_session = st.number_input("Product Detail Views Per App Session", min_value = 0.0)
sales_product_views = st.number_input("Sales Product Views", min_value = 0.0)

# Boolean Inputs conversion
credit_card_info_save = st.selectbox("Credit Card Info Saved?", ["Yes", "No"])
push_status = st.selectbox("Push Notification Status", ["Yes", "No"])

credit_card_info_save = 1 if credit_card_info_save == "Yes" else 0
push_status_bool = 1 if push_status == "Yes" else 0

# Submit Button
if st.button('Predict Churn'):
    data = {
        "session_duration": session_duration,
        "avg_order_value": avg_order_value,
        "customer_service_calls": customer_service_calls,
        "app_transactions": app_transactions,
        "desktop_sessions": desktop_sessions,
        "product_detail_view_per_app_session": product_detail_view_per_app_session,
        "sale_product_views": sales_product_views,
        "credit_card_info_save": credit_card_info_save,
        "push_status": push_status_bool
    }
    
    response = requests.post(API_URL, json=data)
    
    if response.status_code == 200:
        result = response.json()
        st.success(f"Churn Prediction: **{result['Churn Prediction']}** (0 = No Churn, 1 = Churn)")
        st.info(f"Probability: **{result['Churn Probability']}**")
    else:
        st.error("Failed to get prediction from API. Check your backend.")