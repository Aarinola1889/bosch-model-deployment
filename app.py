from flask import Flask, request, jsonify
import pandas as pd
import os
import sys

app = Flask(__name__)

print("🔍 ===== MODEL LOADING DEBUG ======")
print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

# Check if model file exists
model_path = 'bosch_model.joblib'
print(f"Looking for model file: {model_path}")

if os.path.exists(model_path):
    file_size = os.path.getsize(model_path)
    print(f"✅ Model file FOUND: {file_size} bytes")
    
    # Try different loading methods
    try:
        print("🔄 Attempt 1: Loading with joblib...")
        import joblib
        model = joblib.load(model_path)
        model_loaded = True
        print("🎉 Model loaded SUCCESSFULLY with joblib!")
        
    except Exception as e1:
        print(f"❌ Joblib failed: {e1}")
        
        try:
            print("🔄 Attempt 2: Loading with pickle...")
            import pickle
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            model_loaded = True
            print("🎉 Model loaded SUCCESSFULLY with pickle!")
            
        except Exception as e2:
            print(f"❌ Pickle failed: {e2}")
            model_loaded = False
            model = None
            
else:
    print("❌ Model file NOT FOUND!")
    model_loaded = False
    model = None

print(f"Final model_loaded status: {model_loaded}")
print("===== END DEBUG ======")

@app.route('/')
def home():
    status = "✅ FULLY OPERATIONAL" if model_loaded else "❌ MODEL LOADING FAILED"
    return f"""
    <html>
        <head>
            <title>Bosch Demand Prediction</title>
            <style>
                body {{ font-family: Arial; margin: 40px; }}
                .success {{ color: green; font-weight: bold; }}
                .error {{ color: red; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>🚀 Bosch Demand Prediction API</h1>
            <p>Status: <span class="{'success' if model_loaded else 'error'}">{status}</span></p>
            <p><a href="/health">Health Check</a> | <a href="/test">Test Prediction</a></p>
            <p><em>Check Render logs for detailed debugging information</em></p>
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

@app.route('/test')
def test_page():
    return """
    <html>
        <body style="font-family: Arial; margin: 40px;">
            <h1>Test Prediction</h1>
            <p>Use this curl command to test:</p>
            <pre>
curl -X POST https://bosch-model-api.onrender.com/predict \\
  -H "Content-Type: application/json" \\
  -d '{
    "throughput_rate": 245,
    "downtime_minutes": 15,
    "inventory_level": 12500,
    "supplier_lead_time_days": 7,
    "defect_rate": 1.2,
    "iot_sensor_reading": 0.87,
    "temperature_c": 22.4,
    "humidity_percent": 45
  }'
            </pre>
        </body>
    </html>
    """

@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({
            'error': 'Model not loaded - check server logs for details',
            'status': 'failed',
            'debug_info': 'Model file exists but cannot be loaded'
        }), 500
    
    try:
        data = request.json
        
        # Create DataFrame for prediction
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
