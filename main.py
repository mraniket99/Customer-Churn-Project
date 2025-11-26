from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

model = joblib.load('model/churn_pred_cl.pkl')

class ChurnInput(BaseModel):
    
    session_duration: float
    avg_order_value: float
    customer_service_calls:float
    app_transactions:float
    desktop_sessions:float
    product_detail_view_per_app_session: float
    sale_product_views: float
    credit_card_info_save: float
    push_status: float
    

@app.get('/')
def welcome():
    return "Churn Prediction API"
    
@app.post('/predict')
def predict_churn(data: ChurnInput):
    
    # Convert String to integers
    credit = 1 if data.credit_card_info_save == "Yes" else 0
    push = 1 if data.push_status == "Yes" else 0
    
    # Create feature array
    features = np.array([[data.session_duration, data.avg_order_value,
                        data.customer_service_calls, data.app_transactions, 
                        data.desktop_sessions, data.product_detail_view_per_app_session,
                        data.sale_product_views, credit, push]])
    
    prediction = model.predict(features)[0]
    prob = model.predict_proba(features)[0][1]
    
    return {"Churn Prediction": int(prediction),
            "Churn Probability": round(float(prob), 2)}