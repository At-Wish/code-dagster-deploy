"""
Project A: Data Pipeline for ETL Operations
This project handles data extraction, transformation, and loading operations.
"""

from dagster import Definitions, job, op, AssetMaterialization, AssetKey
from dagster._core.definitions import asset
import pandas as pd
import logging

logger = logging.getLogger(__name__)

@op
def extract_data():
    """Extract data from source systems."""
    logger.info("Extracting data from source systems...")
    # Simulate data extraction
    data = {"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "value": [100, 200, 300]}
    df = pd.DataFrame(data)
    
    yield AssetMaterialization(
        asset_key=AssetKey("raw_data"),
        description="Raw data extracted from source systems"
    )
    
    return df

@op
def transform_data(df):
    """Transform the extracted data."""
    logger.info("Transforming data...")
    # Add a new column
    df["processed_value"] = df["value"] * 1.1
    
    yield AssetMaterialization(
        asset_key=AssetKey("processed_data"),
        description="Data after transformation"
    )
    
    return df

@op
def load_data(df):
    """Load the transformed data to destination."""
    logger.info("Loading data to destination...")
    # Simulate data loading
    logger.info(f"Loaded {len(df)} records to destination")
    
    yield AssetMaterialization(
        asset_key=AssetKey("loaded_data"),
        description="Data loaded to destination system"
    )
    
    return len(df)

@job
def etl_pipeline():
    """Main ETL pipeline job."""
    df = extract_data()
    transformed_df = transform_data(df)
    load_data(transformed_df)

@asset
def daily_summary():
    """Generate daily summary statistics."""
    logger.info("Generating daily summary...")
    return {"total_records": 1000, "success_rate": 0.95, "avg_processing_time": 2.5}

defs = Definitions(
    jobs=[etl_pipeline],
    assets=[daily_summary],
)
