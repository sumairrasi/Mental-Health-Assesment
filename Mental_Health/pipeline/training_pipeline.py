import sys
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.components.data_ingestion import DataIngestion
from Mental_Health.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig
from Mental_Health.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from Mental_Health.components.data_validation import DataValidation
from Mental_Health.components.data_transformation import DataTrasnformation
class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        
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
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact) -> DataTransformationArtifact:
        try:
            data_transformation = DataTrasnformation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_transformation_config=self.data_transformation_config,
                data_validation_artifact=data_validation_artifact
            )
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)
        
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(
                data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact
            )
            
        except Exception as e:
            raise MentalHealthException(e,sys)
    