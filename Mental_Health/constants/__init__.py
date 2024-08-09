import os
from datetime import time

DATABASE_NAME ="MENTAL_HEALTH"

COLLECTION_NAME = "mental_health"

MONGODB_URL_KEY = "MONGODB_URL"

PIPELINE_NAME:str = "mentalhealth"
ARTIFACT_DIR:str = "artifact"
FILE_NAME:str = "survey.csv"
MODEL_FILE_NAME = "model.pkl"
TRAIN_FILE_NAME:str = "train.csv"
TEST_FILE_NAME:str = "test.csv"



# Data Ingestion related Constant

DATA_INGESTION_COLLECTION_NAME: str = "mental_health"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2