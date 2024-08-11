import os
import sys
from pandas import DataFrame
import pandas as pd
from sklearn.model_selection import train_test_split

from Mental_Health.entity.config_entity import DataIngestionConfig
from Mental_Health.entity.artifact_entity import DataIngestionArtifact
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.data_access.mentalhealth_data import Mental_Health_Data
from Mental_Health.configuration.progressbar import ProgressBarManager

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
            self.progress_bar = ProgressBarManager()
        except Exception as e:
            raise MentalHealthException(e,sys)
    
    def export_data_into_feature_shape(self) ->DataFrame:
        try:
            logging.info("Exporting data from database")
            mentalhealth_data = Mental_Health_Data()
            self.progress_bar.update(1)
            dataframe = mentalhealth_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)
            logging.info(f"shape of dataframe: {dataframe.shape}")
            self.progress_bar.update(1)
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            self.progress_bar.update(1)
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"saving exported data into feature store file path: {feature_store_file_path}")
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        
        except Exception as e:
            raise MentalHealthException(e,sys)
    
    def split_data_train_test(self,dataframe: DataFrame) -> None:
        
        logging.info("Entered split data into train and test method of data ingestion class")
        try:
            logging.info(f"dataframe: {dataframe} and columns: {dataframe.columns}")
            self.progress_bar.update(1)
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            self.progress_bar.update(1)
            logging.info("performed train test split on the dataframe")
            logging.info("Exited split train test method of Data ingestion class")
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Exporting train and test file")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)
            self.progress_bar.update(1)
        except Exception as e:
            MentalHealthException(e,sys)
        
    
    def initiate_data_ingestion(self) ->DataIngestionArtifact:
        
        try:
            total_steps = 6
            self.progress_bar.initialize(total_steps, title="Data Ingestion Process")
            logging.info("Entered initiate method of data ingestion")
            dataframe = self.export_data_into_feature_shape()       
            logging.info("got the data from database")
            self.split_data_train_test(dataframe)
            logging.info("Exited from data ingestion")
            data_ingestion_artifact = DataIngestionArtifact(training_file_path=self.data_ingestion_config.training_file_path,
                                                            testing_file_path=self.data_ingestion_config.testing_file_path)
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            self.progress_bar.finish()
            return data_ingestion_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)
        
        