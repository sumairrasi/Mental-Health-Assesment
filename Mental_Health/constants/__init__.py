import os
from datetime import time,date

DATABASE_NAME ="Mental_Health"

COLLECTION_NAME = "mental_health"

MONGODB_URL_KEY = "MONGODB_URL"

PIPELINE_NAME:str = "mentalhealth"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "survey.csv"
MODEL_FILE_NAME = "model.pkl"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"


TARGET_COLUMN = "treatment"
CURRENT_YEAR = date.today().year
PREPROCESSING_OBJECT_FILE_NAME = "Processing.pkl"
SCHEMA_FILE_PATH = os.path.join("config","schema.yaml")

# Data Ingestion related Constant

DATA_INGESTION_COLLECTION_NAME: str = "mental_health"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2


DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"