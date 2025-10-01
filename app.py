from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import os

app = Flask(__name__)

# Try to load model with basic joblib (no scikit-learn dependency for inference)
try:
    import joblib
    model = joblib.load('bosch_model.joblib')
    model_loaded = True
    print("✅ Model loaded successfully")
except Exception as e:
    model_loaded = False
    print(f"❌ Model loading failed: {e}")

@app.route('/')
def home():
    return """
    <html>
        <body style="font-family: Arial; margin: 40px;">
            <h1>🚀 Bosch Demand Prediction API</h1>
            <p>Model Loaded: <strong>""" + str(model_loaded) + """</strong></p>
            <p><a href="/health">Check Health</a></p>
        </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "service": "Bosch Demand Predictor",
        "version": "1.0"
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({'error': 'Model not loaded', 'status': 'failed'}), 500
    
    try:
        data = request.json
        
        # Create DataFrame for prediction
        input_data = pd.DataFrame([[
            float(data['throughput_rate']),
            float(data['downtime_minutes']), 
            float(data['inventory_level']),
            float(data['supplier_lead_time_days']),
            float(data['defect_rate']),
            float(data['iot_sensor_reading']),
            float(data['temperature_c']),
            float(data['humidity_percent'])
        ]], columns=['throughput_rate', 'downtime_minutes', 'inventory_level',
                    'supplier_lead_time_days', 'defect_rate', 'iot_sensor_reading',
                    'temperature_c', 'humidity_percent'])
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        return jsonify({
            'prediction': float(prediction),
            'status': 'success',
            'model': 'Bosch Demand Predictor v1.0'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
