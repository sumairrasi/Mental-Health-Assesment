from Mental_Health.configuration.mongodb_connection import MongoDBClient
from Mental_Health.constants import DATABASE_NAME
from Mental_Health.exception import MentalHealthException
import pandas as pd
import sys
from typing import Optional
import numpy as np

class Mental_Health_Data:
    
    
    def __init__(self):
        
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MentalHealthException(e,sys)
        
        
    def export_collection_as_dataframe(self, collection_name:str, database_name:Optional[str]=None) -> pd.DataFrame:
        try:
            if database_name is None:
                print(collection_name)
                print("Database: ", self.mongo_client.database_name)
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]
            
            df = pd.DataFrame(list(collection.find()))
            if '_id' in df.columns.to_list():
                df.drop('_id', axis=1,inplace=True)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise MentalHealthException(e,sys)
