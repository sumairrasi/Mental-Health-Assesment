import numpy as np 
import pandas as pd 
from sklearn.preprocessing import OrdinalEncoder, PowerTransformer, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from Mental_Health.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from Mental_Health.entity.config_entity import DataTransformationConfig
from Mental_Health.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact, DataValidationArtifact
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns
from Mental_Health.entity.estimator import TargetValueMapping
from Mental_Health.configuration.progressbar import ProgressBarManager
import sys
pd.set_option('future.no_silent_downcasting', True)
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

class DataTrasnformation:
    
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
            self.progress_bar = ProgressBarManager()
        
        except Exception as e:
            raise MentalHealthException(e, sys)
        
        
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
            
        except Exception as e:
            raise MentalHealthException(e,sys)
    @staticmethod
    def get_data_null_handler(df: pd.DataFrame, data_null_handler: dict) -> pd.DataFrame:
        logging.info(" Entered data null handler in transformation class")
        try:
            for column, replacement in data_null_handler['data_null_handler'].items():
                if column in df.columns:
                    df[column] = df[column].replace('Unknown', replacement[0])
            return df
        except Exception as e:
            raise MentalHealthException(e,sys)
        
    def get_data_transformation_object(self)-> Pipeline:
        
        logging.info(" Entered data transformation object in transformation class")
        
        try:
            logging.info("got catgorical columns from schema config")
            od_encoder = OrdinalEncoder()
            lb_en_columns = self._schema_config['lb_en_columns']
            transform_columns = self._schema_config['transform_columns']
            logging.info("Initializing label encoding")
            transform_pipe = Pipeline(steps=[
                ('transformer',PowerTransformer(method='yeo-johnson'))
            ])
            logging.info(f"label encoding columns: {lb_en_columns}")
            preprocessor = ColumnTransformer(
                [
                    ('LabelEncoder',od_encoder,lb_en_columns),
                    ('Transformer',transform_pipe,transform_columns)
                ]
            )
            logging.info("created preprocessor object from columnTransformer")
            self.progress_bar.update(1)
            logging.info("Exited data transformation class")
            
            return preprocessor
        
        except Exception as e:
            raise MentalHealthException(e, sys)
        
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if self.data_validation_artifact.validation_status:
                total_steps = 9
                self.progress_bar.initialize(total_steps, title="Data validation Process")
                
                logging.info("Starting data transformation")
                preprocessor = self.get_data_transformation_object()
                self.progress_bar.update(1)
                logging.info("Got the processor object")
                
                train_df = DataTrasnformation.read_data(file_path=self.data_ingestion_artifact.training_file_path)
                test_df = DataTrasnformation.read_data(file_path=self.data_ingestion_artifact.testing_file_path)
                self.progress_bar.update(1)
                logging.info("Starting data null handling")
                train_df = DataTrasnformation.get_data_null_handler(train_df,self._schema_config)
                test_df = DataTrasnformation.get_data_null_handler(test_df,self._schema_config)
                input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
                target_feature_train_df = train_df[TARGET_COLUMN]
                
                logging.info("Got train features and test features of training dataset")
                
                drop_cols = self._schema_config['drop_columns']
                self.progress_bar.update(1)
                logging.info("drop the columns in drop_cols in training dataset")
                
                input_feature_train_df = drop_columns(df=input_feature_train_df, cols=drop_cols)
                logging.info(f"input_feature_train_df: {len(input_feature_train_df.columns)}")
                target_feature_train_df = target_feature_train_df.replace(
                    TargetValueMapping()._asdict()
                )
                self.progress_bar.update(1)
                input_features_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
                
                target_feature_test_df = test_df[TARGET_COLUMN]
                
                input_features_test_df = drop_columns(df=input_features_test_df,cols= drop_cols)
                logging.info(f"input_features_test_df: {len(input_features_test_df.columns)}")
                logging.info(f"Input train features shape: {input_feature_train_df.columns}")
                logging.info(f"Input test features shape: {input_features_test_df.columns}")
                logging.info("dropped the column in drop_col of test dataset")
                
                target_feature_test_df = target_feature_test_df.replace(
                    TargetValueMapping()._asdict()
                )
                
                logging.info("Got the train and test features of dataset")
                
                
                logging.info("Applying proprocessing object on training dataframe and test dataframe")
                self.progress_bar.update(1)
                # print(input_feature_train_df)
                input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
                logging.info(f"input_feature_train_arr :",input_feature_train_arr.shape)
                logging.info("Used the preprocess feature fit transform the train features")
                
                input_feature_test_arr = preprocessor.fit_transform(input_features_test_df)
                
                logging.info("Creating train array and test array")
                
                train_arr = np.c_[
                    input_feature_train_arr,np.array(target_feature_train_df)
                ]
                
                test_arr = np.c_[
                    input_feature_test_arr,np.array(target_feature_test_df)
                ]
                logging.info(f"train array shape: {train_arr.shape}")
                logging.info(f"test array shape: {test_arr.shape}")
                
                self.progress_bar.update(1)
                save_object(self.data_transformation_config.transformed_object_file_path,preprocessor)
                save_numpy_array_data(self.data_transformation_config.transformation_train_file_path,array=train_arr)
                save_numpy_array_data(self.data_transformation_config.transformation_test_file_path,array=test_arr)
                self.progress_bar.update(1)
                logging.info("saved the preprocessor object")
                
                logging.info("Exited the initiate data transformation class")
                
                
                data_transformation_artifact = DataTransformationArtifact(
                    transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                    transformed_train_file_path=self.data_transformation_config.transformation_train_file_path,
                    transformed_test_file_path=self.data_transformation_config.transformation_test_file_path
                )
                self.progress_bar.update(1)
                self.progress_bar.finish()
                return data_transformation_artifact
            
            else:
                raise Exception(self.data_validation_artifact.message)
        except Exception as e:
            raise MentalHealthException(e,sys)