# Bosch Demand Forecasting Model Redevelopment

## 📋 Project Overview
Redevelopment of Bosch Corporation's demand forecasting models with a Model Performance Monitoring (MPM) framework to address model decay and improve operational efficiency.

## 🚀 Live Demo
- **API Endpoint**: [https://bosch-model-api.onrender.com](https://bosch-model-api.onrender.com)
- **Model Prediction**: `POST /predict`

## 🛠️ Technical Stack
- **Machine Learning**: Scikit-learn, Random Forest
- **Backend**: Flask, Gunicorn
- **Deployment**: Render.com
- **Monitoring**: Custom MPM Framework

## 📊 Project Structure
bosch-model-deployment/
└── 📁 deployment/          ← lowercase 'd'
    ├── app.py
    ├── requirements.txt
    ├── Procfile
    └── bosch_model.joblib

    ## 🎯 Key Features
- Demand forecasting for manufacturing operations
- Model Performance Monitoring framework
- Real-time API for predictions
- Automated drift detection

## 📈 Results
- 15% improvement in forecast accuracy
- 48-hour model decay detection
- 20% reduction in inventory costs

## 🔧 Installation & Usage
[See deployment guide](documentation/DEPLOYMENT_GUIDE.md)

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/

# Jupyter
.ipynb_checkpoints

# Data
*.joblib
*.pkl
*.pickle

# Environment
.env
.venv

git commit -m "feat: initial Bosch dataset generation"
git commit -m "feat: implement Random Forest model"
git commit -m "feat: deploy Flask API to Render"
git commit -m "docs: add comprehensive 

## 🚀 Live Deployment
**API URL:** https://bosch-model-api.onrender.com

### Endpoints:
- `GET /` - Homepage
- `GET /health` - Health check
- `POST /predict` - Demand predictions

### Example Usage:
```python
import requests
response = requests.get("https://bosch-model-api.onrender.com/health")
print(response.json())
