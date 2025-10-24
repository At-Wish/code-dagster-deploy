"""
Project C: Machine Learning Pipeline
This project handles ML model training, validation, and deployment.
"""

from dagster import Definitions, job, op, AssetMaterialization, AssetKey, sensor, RunRequest, SkipReason, AutoMaterializePolicy
from dagster._core.definitions import asset
import pandas as pd
import numpy as np
import logging
from datetime import datetime, timedelta
import json

logger = logging.getLogger(__name__)

@op
def prepare_training_data():
    """Prepare data for model training."""
    logger.info("Preparing training data...")
    
    # Generate synthetic training data
    np.random.seed(42)
    n_samples = 1000
    X = np.random.randn(n_samples, 5)
    y = np.random.randint(0, 2, n_samples)
    
    training_data = {
        "features": X.tolist(),
        "labels": y.tolist(),
        "n_samples": n_samples,
        "feature_names": ["feature_1", "feature_2", "feature_3", "feature_4", "feature_5"]
    }
    
    yield AssetMaterialization(
        asset_key=AssetKey("training_data"),
        description="Prepared training dataset"
    )
    
    return training_data

@op
def train_model(training_data):
    """Train machine learning model."""
    logger.info("Training ML model...")
    
    # Simulate model training
    model_info = {
        "model_type": "RandomForest",
        "accuracy": 0.85,
        "precision": 0.82,
        "recall": 0.88,
        "f1_score": 0.85,
        "training_time": "2.5 minutes",
        "model_version": "v1.0.0"
    }
    
    yield AssetMaterialization(
        asset_key=AssetKey("trained_model"),
        description="Trained ML model with performance metrics"
    )
    
    return model_info

@op
def validate_model(model_info):
    """Validate model performance."""
    logger.info("Validating model performance...")
    
    validation_results = {
        "validation_accuracy": 0.83,
        "validation_precision": 0.81,
        "validation_recall": 0.86,
        "validation_f1_score": 0.83,
        "validation_status": "passed",
        "validation_timestamp": datetime.now().isoformat()
    }
    
    yield AssetMaterialization(
        asset_key=AssetKey("model_validation"),
        description="Model validation results"
    )
    
    return validation_results

@op
def deploy_model(model_info, validation_results):
    """Deploy validated model."""
    logger.info("Deploying model to production...")
    
    if validation_results["validation_status"] == "passed":
        deployment_info = {
            "deployment_status": "successful",
            "model_version": model_info["model_version"],
            "deployment_timestamp": datetime.now().isoformat(),
            "endpoint_url": "https://api.example.com/ml/predict"
        }
        
        yield AssetMaterialization(
            asset_key=AssetKey("deployed_model"),
            description="Model deployed to production"
        )
        
        return deployment_info
    else:
        logger.error("Model validation failed, skipping deployment")
        return {"deployment_status": "failed", "reason": "validation_failed"}

@job
def ml_pipeline():
    """Machine learning pipeline."""
    training_data = prepare_training_data()
    model_info = train_model(training_data)
    validation_results = validate_model(model_info)
    deploy_model(model_info, validation_results)

@asset(auto_materialize_policy=AutoMaterializePolicy.eager())
def model_performance_metrics():
    """Track model performance over time with auto-materialization."""
    logger.info("Updating model performance metrics...")
    return {
        "current_accuracy": 0.85,
        "drift_detected": False,
        "last_retrain": datetime.now().isoformat(),
        "prediction_count": 10000
    }

@sensor(job=ml_pipeline)
def data_drift_sensor(context):
    """Sensor to detect data drift and trigger retraining."""
    # Simulate drift detection logic
    drift_detected = np.random.random() < 0.1  # 10% chance of drift
    
    if drift_detected:
        logger.warning("Data drift detected, triggering model retraining")
        return RunRequest(run_key=f"drift_retrain_{datetime.now().timestamp()}")
    else:
        return SkipReason("No data drift detected")

defs = Definitions(
    jobs=[ml_pipeline],
    assets=[model_performance_metrics],
    sensors=[data_drift_sensor],
)
