"""
Project B: Analytics and Reporting Pipeline
This project handles data analytics, reporting, and dashboard updates.
"""

from dagster import Definitions, job, op, AssetMaterialization, AssetKey, schedule, RunRequest, sensor, SensorEvaluationContext
from dagster._core.definitions import asset
import pandas as pd
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

@op
def fetch_analytics_data():
    """Fetch data for analytics processing."""
    logger.info("Fetching analytics data...")
    # Simulate fetching analytics data
    data = {
        "date": ["2024-01-01", "2024-01-02", "2024-01-03"],
        "revenue": [10000, 12000, 15000],
        "users": [1000, 1200, 1500],
        "conversion_rate": [0.05, 0.06, 0.07]
    }
    df = pd.DataFrame(data)
    
    yield AssetMaterialization(
        asset_key=AssetKey("analytics_raw_data"),
        description="Raw analytics data fetched from various sources"
    )
    
    return df

@op
def calculate_metrics(df):
    """Calculate key business metrics."""
    logger.info("Calculating business metrics...")
    
    metrics = {
        "total_revenue": df["revenue"].sum(),
        "avg_revenue_per_user": df["revenue"].sum() / df["users"].sum(),
        "avg_conversion_rate": df["conversion_rate"].mean(),
        "revenue_growth": ((df["revenue"].iloc[-1] - df["revenue"].iloc[0]) / df["revenue"].iloc[0]) * 100
    }
    
    yield AssetMaterialization(
        asset_key=AssetKey("business_metrics"),
        description="Calculated business metrics"
    )
    
    return metrics

@op
def generate_report(metrics):
    """Generate analytics report."""
    logger.info("Generating analytics report...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics,
        "status": "completed"
    }
    
    yield AssetMaterialization(
        asset_key=AssetKey("analytics_report"),
        description="Generated analytics report"
    )
    
    return report

@job
def analytics_pipeline():
    """Analytics processing pipeline."""
    df = fetch_analytics_data()
    metrics = calculate_metrics(df)
    generate_report(metrics)

@asset
def dashboard_data():
    """Prepare data for dashboard visualization."""
    logger.info("Preparing dashboard data...")
    return {
        "charts": ["revenue_trend", "user_growth", "conversion_funnel"],
        "last_updated": datetime.now().isoformat(),
        "data_points": 1000
    }

@schedule(cron_schedule="0 6 * * *", job=analytics_pipeline)
def daily_analytics_schedule(context):
    """Schedule analytics pipeline to run daily at 6 AM."""
    return RunRequest(run_key=f"daily_analytics_{context.scheduled_execution_time}")

@sensor(job=analytics_pipeline)
def data_quality_sensor(context: SensorEvaluationContext):
    """Sensor that triggers analytics pipeline when data quality issues are detected."""
    # Simulate checking for data quality issues
    # In a real scenario, this would check external systems or databases
    current_hour = datetime.now().hour
    
    # Trigger every 4 hours for demonstration
    if current_hour % 4 == 0:
        return RunRequest(
            run_key=f"data_quality_check_{current_hour}",
            tags={"trigger": "data_quality_sensor"}
        )
    
    return None

defs = Definitions(
    jobs=[analytics_pipeline],
    assets=[dashboard_data],
    schedules=[daily_analytics_schedule],
    sensors=[data_quality_sensor],
)
