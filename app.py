#!/usr/bin/env python
# coding: utf-8

# In[1]:


from flask import Flask, request, jsonify
import joblib
import os


# In[3]:


app = Flask(__name__)


# In[5]:


MODEL_PATH = "sarima_model.pkl"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"{MODEL_PATH} not found in project folder.")
model = joblib.load(MODEL_PATH)
print("Model loaded successfully!")


# In[6]:


@app.route("/")
def home():
    return "Reliance Stock Price Forecast API is running successfully!"


# In[7]:


@app.route("/forecast", methods=["POST"])
def forecast():
    try:
        data = request.get_json()
        # Default forecast = 30 days
        steps = int(data.get("steps", 30))
        # Generate forecast
        prediction = model.forecast(steps=steps)
        # Convert to list for JSON response
        prediction_list = prediction.tolist()
        return jsonify({
            "status": "success",
            "forecast_days": steps,
            "predicted_prices": prediction_list
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


# In[8]:


if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:




