from flask import Flask, request, jsonify
import joblib
import pandas as pd
import os

app = Flask(__name__)

# Load model directly with joblib
try:
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
            <p>Model Status: <strong>""" + ("✅ LOADED" if model_loaded else "❌ FAILED") + """</strong></p>
            <p><a href="/health">Health Check</a></p>
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
        
        # Convert input to DataFrame
        input_data = pd.DataFrame([[
            float(data['throughput_rate']),
            float(data['downtime_minutes']), 
            float(data['inventory_level']),
            float(data['supplier_lead_time_days']),
            float(data['defect_rate']),
            float(data['iot_sensor_reading']),
            float(data['temperature_c']),
            float(data['humidity_percent'])
        ]])
        
        # Make prediction (assuming model has predict method)
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
