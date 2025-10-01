from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Debug model loading
print("🔍 Starting model load...")
print(f"Current directory: {os.getcwd()}")
print(f"Files in directory: {os.listdir('.')}")

try:
    import joblib
    print("✅ Joblib imported successfully")
    
    # Check if model file exists
    if os.path.exists('bosch_model.joblib'):
        file_size = os.path.getsize('bosch_model.joblib')
        print(f"✅ Model file exists: {file_size} bytes")
        
        # Try to load the model
        model = joblib.load('bosch_model.joblib')
        model_loaded = True
        print("🎉 Model loaded successfully!")
        
    else:
        print("❌ Model file NOT FOUND")
        model_loaded = False
        
except Exception as e:
    print(f"❌ Model loading failed: {e}")
    model_loaded = False

@app.route('/')
def home():
    status = "✅ LOADED" if model_loaded else "❌ FAILED"
    return f"""
    <html>
        <body style="font-family: Arial; margin: 40px;">
            <h1>🚀 Bosch Demand Prediction API</h1>
            <p>Model Status: <strong>{status}</strong></p>
            <p>Check the Render logs for detailed loading information</p>
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
        return jsonify({'error': 'Model not loaded - check server logs', 'status': 'failed'}), 500
    
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
