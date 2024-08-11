import json
import sys

import pandas as pd
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

from pandas import DataFrame
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.utils.main_utils import read_yaml_file, write_yaml_file
from Mental_Health.entity.config_entity import DataIngestionConfig,DataValidationConfig
from Mental_Health.constants import SCHEMA_FILE_PATH
from Mental_Health.entity.artifact_entity import DataValidationArtifact
from Mental_Health.configuration.progressbar import ProgressBarManager


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionConfig, data_validation_config: DataValidationConfig):
        
        try:
            self.progress_bar = ProgressBarManager()
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise MentalHealthException(e,sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config['columns'])
            logging.info(f" Is required column present: [{status}]")
            return status
        except Exception as e:
            raise MentalHealthException(e,sys)
        
    
    def is_column_exist(self, df: DataFrame) -> bool:
        try:
            data_frame_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []
            for column in self._schema_config['numerical_columns']:
                if column not in data_frame_columns:
                    missing_numerical_columns.append(column)
            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical column: {missing_numerical_columns}")
            
            for column in self._schema_config['categorical_columns']:
                if column not in data_frame_columns:
                    missing_categorical_columns.append(column)
            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical column: {missing_categorical_columns}")
                
            return False if len(missing_numerical_columns)>0 or len(missing_categorical_columns)>0 else True
                
        except Exception as e:
            raise MentalHealthException(e,sys)

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            MentalHealthException(e,sys)
            
    def detect_dataset_drift(self, reference_df: DataFrame, current_df:DataFrame) -> bool:
        
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            self.progress_bar.update(1)
            data_drift_profile.calculate(reference_df,current_df)
            self.progress_bar.update(1)
            report = data_drift_profile.json()
            json_report = json.loads(report)
            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path,content=json_report)
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]
            logging.info(f"{n_drifted_features}/{n_features} drift detected")
            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            self.progress_bar.update(1)
            return drift_status
        except Exception as e:
            raise MentalHealthException(e,sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            total_steps = 7
            self.progress_bar.initialize(total_steps, title="Data validation Process")
            validation_error_msg = ""
            logging.info("Starting data validation")
            self.progress_bar.update(1)
            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.training_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.testing_file_path))
            status = self.validate_number_of_columns(dataframe=train_df)
            self.progress_bar.update(1)
            logging.info(f"All required columns present in the train dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in the training dataframe."
            status = self.validate_number_of_columns(dataframe=test_df)
            logging.info(f"All required columns  present in the test dataframe: {status}")
            if not status:
                validation_error_msg += f"Columns are missing in the test dataframe."
            status = self.is_column_exist(df=train_df)
            if not status:
                validation_error_msg += f"Columns are missing in the training dataframe."
            
            status = self.is_column_exist(df=test_df)
            if not status:
                validation_error_msg += f"Columns are missing in the test dataframe."
            
            validation_status = len(validation_error_msg) == 0
            if validation_status:
                drift_status = self.detect_dataset_drift(train_df,test_df)
                self.progress_bar.update(1)
                if drift_status:
                    logging.info(f"Drift detected")
                    validation_err_msg = "Drift detected"
                else:
                    validation_err_msg = "Drift not detected"
            else:
                logging.info(f"Validation error: {validation_err_msg}")
                self.progress_bar.update(1)
            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_err_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            self.progress_bar.finish()
            return data_validation_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)