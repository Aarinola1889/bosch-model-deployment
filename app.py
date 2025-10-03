
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the model
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
        <head>
            <title>Bosch Demand Prediction API</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f0f2f5; }
                .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
                .endpoint { background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #3498db; }
                code { background: #2c3e50; color: white; padding: 10px; border-radius: 4px; display: block; overflow-x: auto; }
                .status { padding: 5px 10px; border-radius: 4px; font-weight: bold; }
                .healthy { background: #d4edda; color: #155724; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Bosch Demand Prediction API</h1>
                <p>This API predicts manufacturing demand based on operational data for Bosch Corporation.</p>
                
                <div class="endpoint">
                    <h3>📊 API Status</h3>
                    <p><span class="status healthy">✅ OPERATIONAL</span></p>
                    <p>Model Loaded: <strong>""" + str(model_loaded) + """</strong></p>
                </div>

                <div class="endpoint">
                    <h3>🔧 Health Check</h3>
                    <p><strong>Endpoint:</strong> <code>GET /health</code></p>
                    <p><a href="/health" target="_blank">Test Health Check →</a></p>
                </div>

                <div class="endpoint">
                    <h3>🎯 Make Prediction</h3>
                    <p><strong>Endpoint:</strong> <code>POST /predict</code></p>
                    <p>Submit manufacturing data to get demand predictions.</p>
                </div>

                <div class="endpoint">
                    <h3>📝 Example Usage (Python)</h3>
                    <code>
import requests

url = "https://bosch-model-api.onrender.com/predict"
data = {
    "throughput_rate": 245,
    "downtime_minutes": 15,
    "inventory_level": 12500,
    "supplier_lead_time_days": 7,
    "defect_rate": 1.2,
    "iot_sensor_reading": 0.87,
    "temperature_c": 22.4,
    "humidity_percent": 45
}

response = requests.post(url, json=data)
print(response.json())
                    </code>
                </div>

                <div class="endpoint">
                    <h3>🛠️ Project Info</h3>
                    <p><strong>Project:</strong> Bosch Model Redevelopment</p>
                    <p><strong>Model:</strong> Random Forest Regressor</p>
                    <p><strong>Framework:</strong> Flask + Scikit-learn</p>
                    <p><strong>Deployment:</strong> Render.com</p>
                </div>
            </div>
        </body>
    </html>
    """

@app.route('/health')
def health():
    status = "healthy" if model_loaded else "degraded"
    return jsonify({
        "status": status,
        "model_loaded": model_loaded,
        "service": "Bosch Demand Predictor API",
        "version": "1.0",
        "endpoints": {
            "home": "GET /",
            "health": "GET /health", 
            "predict": "POST /predict"
        }
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({'error': 'Model not loaded', 'status': 'failed'}), 500
    
    try:
        # Get data from request
        data = request.json
        
        if not data:
            return jsonify({'error': 'No JSON data provided', 'status': 'failed'}), 400
        
        # Validate required fields
        required_fields = ['throughput_rate', 'downtime_minutes', 'inventory_level',
                          'supplier_lead_time_days', 'defect_rate', 'iot_sensor_reading',
                          'temperature_c', 'humidity_percent']
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing fields: {missing_fields}', 'status': 'failed'}), 400
        
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
        ]], columns=required_fields)
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        
        return jsonify({
            'prediction': float(prediction),
            'status': 'success',
            'model': 'Bosch Demand Predictor v1.0',
            'units': 'demand_units',
            'input_features': required_fields
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
