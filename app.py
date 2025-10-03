from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Load the COMPATIBLE model
try:
    import joblib
    model = joblib.load('bosch_model_compatible.joblib')
    model_loaded = True
    print("✅ COMPATIBLE MODEL LOADED SUCCESSFULLY!")
except Exception as e:
    model_loaded = False
    print(f"❌ Model loading failed: {e}")

@app.route('/')
def home():
    status = "✅ FULLY OPERATIONAL" if model_loaded else "❌ MODEL FAILED"
    return f"""
    <html>
        <body style="font-family: Arial; margin: 40px;">
            <h1>🚀 Bosch Demand Prediction API</h1>
            <p>Status: <strong>{status}</strong></p>
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
        input_data = pd.DataFrame([[
            data['throughput_rate'],
            data['downtime_minutes'], 
            data['inventory_level'],
            data['supplier_lead_time_days'],
            data['defect_rate'],
            data['iot_sensor_reading'],
            data['temperature_c'],
            data['humidity_percent']
        ]], columns=['throughput_rate', 'downtime_minutes', 'inventory_level',
                    'supplier_lead_time_days', 'defect_rate', 'iot_sensor_reading',
                    'temperature_c', 'humidity_percent'])
        
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
