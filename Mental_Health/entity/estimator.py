import sys
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging


class TargetValueMapping:
    def __init__(self):
        self.Yes: int = 0
        self.No: int = 1
    
    def _asdict(self):
        return self.__dict__
    
    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(),mapping_response.keys()))
    

class MentalHealthModel:
    def __init__(self,preprocessing_object: Pipeline, trained_model_object: object):
        
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object
        
    def predict(self, dataframe: DataFrame) -> DataFrame:
        logging.info("Entered Predict medthod of Mental Health model class")
        try:
            logging.info("Using Trained model to get predictions")
            transformed_features = self.preprocessing_object.transform(dataframe)
            logging.info("Used Trained model to get predictions")
            return self.trained_model_object.predict(transformed_features)
        except Exception as e:
            raise MentalHealthException(e,sys)