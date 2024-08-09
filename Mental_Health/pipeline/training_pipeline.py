import sys
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.components.data_ingestion import DataIngestion
from Mental_Health.entity.config_entity import DataIngestionConfig
from Mental_Health.entity.artifact_entity import DataIngestionArtifact


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        
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
        
    def run_pipeline(self)->None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
        except Exception as e:
            raise MentalHealthException(e,sys)
    