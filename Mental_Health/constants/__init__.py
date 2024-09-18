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



AWS_ACCESS_KEY_ID_ENV_KEY = "AWS_ACCESS_KEY_ID"
AWS_SECRET_ACCESS_KEY_ENV_KEY = "AWS_SECRET_ACCESS_KEY"
REGION_NAME = "us-east-1"
# Data Ingestion related Constant

DATA_INGESTION_COLLECTION_NAME: str = "mental_health"
DATA_INGESTION_DIR_NAME:str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str = "feature_store"
DATA_INGESTION_INGESTED_DIR:str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

# Data validation related Constant
DATA_VALIDATION_DIR_NAME: str = "data_validation"
DATA_VALIDATION_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str = "report.yaml"

# Data transformation related Constant
DATA_TRANSFORMATION_DIR_NAME:str = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR: str = "transformed_object"


# Data trainer Constant
MODEL_TRAINER_DIR_NAME: str = "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR: str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME: str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE: str = 0.6
MODEL_TRAINER_MODEL_CONFIG_FILE_PATH: str = os.path.join("config","model.yaml")


#Model Evaluation Constant
MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE: float = 0.7
MODEL_BUCKET_NAME = "mentalhealth-model2024"
MODEL_PUSHER_S3_KEY = "model-registry"


APP_HOST = "0.0.0.0"
APP_PORT = 8080