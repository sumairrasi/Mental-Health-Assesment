import sys
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.components.data_ingestion import DataIngestion
from Mental_Health.entity.config_entity import DataIngestionConfig, DataValidationConfig
from Mental_Health.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Mental_Health.components.data_validation import DataValidation

class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info("Getting the data from mongodb")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data train and test from db")
            logging.info("Exited from data ingestion from training pipeline")
            
            return data_ingestion_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)
    
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info(f"Entered the data vaidation method of trainingp pipeline")
        try:
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info(f"Performed the data validation operation")
            logging.info(f"Exited the data validatio operation")
            return data_validation_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)
        
        
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
        except Exception as e:
            raise MentalHealthException(e,sys)
    