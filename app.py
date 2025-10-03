from flask import Flask, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

# Load the function-based model
try:
    with open('bosch_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    predict_function = model_data['predict_function']
    model_loaded = True
    print("✅ FUNCTION-BASED MODEL LOADED SUCCESSFULLY!")
    
except Exception as e:
    model_loaded = False
    print(f"❌ Model loading failed: {e}")

@app.route('/')
def home():
    return "🚀 Bosch API - FUNCTION MODEL - " + ("✅ WORKING" if model_loaded else "❌ FAILED")

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy" if model_loaded else "degraded",
        "model_loaded": model_loaded,
        "model_type": "function_based"
    })

@app.route('/predict', methods=['POST'])
def predict():
    if not model_loaded:
        return jsonify({"error": "Model not loaded", "status": "failed"}), 500
    
    try:
        data = request.json
        features = [
            float(data['throughput_rate']),
            float(data['downtime_minutes']), 
            float(data['inventory_level']),
            float(data['supplier_lead_time_days']),
            float(data['defect_rate']),
            float(data['iot_sensor_reading']),
            float(data['temperature_c']),
            float(data['humidity_percent'])
        ]
        
        prediction = predict_function(features)
        
        return jsonify({
            'prediction': float(prediction),
            'status': 'success',
            'model_type': 'function_based'
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'failed'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
