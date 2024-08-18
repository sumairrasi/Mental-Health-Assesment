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
    
    