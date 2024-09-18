import os
import sys
import numpy as np
import pandas as pd
from Mental_Health.entity.config_entity import MentalHealthPredictorConfig
from Mental_Health.entity.s3_estimator import MentalHealthEstimator
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.utils.main_utils import read_yaml_file
from pandas import DataFrame




class MentalhealthData:
    def __init__(self,
                age,
                gender,
                family_history,
                benefits,
                care_options,
                anonymity,
                leave,
                work_interfere,
                remote_work
                ):
        """
        Usvisa Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.age = age
            self.gender = gender
            self.family_history = family_history
            self.benefits = benefits
            self.care_options = care_options
            self.anonymity = anonymity
            self.leave = leave
            self.work_interfere = work_interfere
            self.remote_work = remote_work

        except Exception as e:
            raise MentalHealthException(e, sys) from e

    def get_mentalhealth_input_data_frame(self)-> DataFrame:
        """
        This function returns a DataFrame from USvisaData class input
        """
        try:
            
            usvisa_input_dict = self.get_mentalhealth_data_as_dict()
            return DataFrame(usvisa_input_dict)
        
        except Exception as e:
            raise MentalHealthException(e, sys) from e


    def get_mentalhealth_data_as_dict(self):
        """
        This function returns a dictionary from MentalhealthData class input 
        """
        logging.info("Entered get_usvisa_data_as_dict method as MentalhealthData class")

        try:
            input_data = {
                "work_interfere": [self.work_interfere],
                "benefits": [self.benefits],
                "care_options": [self.care_options],
                "anonymity": [self.anonymity],
                "leave": [self.leave],
                "Gender": [self.gender],
                "remote_work":[self.remote_work],
                "family_history": [self.family_history],
                "Age": [self.age]
                }

            logging.info("Created mental health data dict")

            logging.info("Exited get_mentalhealth_data_as_dict method as MentalhealthData class")

            return input_data

        except Exception as e:
            raise MentalHealthException(e, sys) from e

class MentalHealthClassifier:
    def __init__(self,prediction_pipeline_config: MentalHealthPredictorConfig = MentalHealthPredictorConfig()) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction the value
        """
        try:
            # self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise MentalHealthException(e, sys)


    def predict(self, dataframe) -> str:
        """
        This is the method of USvisaClassifier
        Returns: Prediction in string format
        """
        try:
            logging.info("Entered predict method of USvisaClassifier class")
            model = MentalHealthEstimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )
            result =  model.predict(dataframe)
            
            return result
        
        except Exception as e:
            raise MentalHealthException(e, sys)