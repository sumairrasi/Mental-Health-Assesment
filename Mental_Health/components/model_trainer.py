import sys
from typing import Tuple
import pandas as pd
import numpy as np
from pandas import DataFrame
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from neuro_mf import ModelFactory

from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.utils.main_utils import load_numpy_array_data, read_yaml_file, load_object, save_object
from Mental_Health.entity.config_entity import ModelTrainerConfig
from Mental_Health.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact, ClassificationMetricArtifact
from Mental_Health.entity.estimator import MentalHealthModel


class ModelTrainer:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact,
                 model_trainer_config:ModelTrainerConfig):
        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config = model_trainer_config
        
    def get_model_object_and_report(self,train: np.array, test: np.array) -> Tuple[object,object]:
        try:
            logging.info("Using Hyperparameter tuning to get best model and report")
            model_factory = ModelFactory(model_config_path=self.model_trainer_config.model_config_file_path)
            x_train, y_train, x_test, y_test = train[:,:-1], train[:,-1],test[:,:-1],test[:,-1]
            y_train = y_train.astype(int)
            y_test = y_test.astype(int)
            best_model_detail = model_factory.get_best_model(
                X=x_train,y=y_train,base_accuracy=self.model_trainer_config.expected_accuracy
            )
            model_obj = best_model_detail.best_model
            y_pred = model_obj.predict(x_test)
            
            accuracy = accuracy_score(y_test,y_pred)
            f1 = f1_score(y_test,y_pred)
            precision = precision_score(y_test,y_pred)
            recall = recall_score(y_test,y_pred)
            metric_artifact = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
            
            return best_model_detail,metric_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)
        
    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
            test_arr = load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
            
            best_model_detail, metric_artifact = self.get_model_object_and_report(train=train_arr,test=test_arr)
            logging.info(f"best metric {metric_artifact}")
            preprocessing_obj = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)
            
            if best_model_detail.best_score < self.model_trainer_config.expected_accuracy:
                logging.info("No best model found with score more than base score")
                raise Exception("No best model found with score more than base score")
            mental_health_model = MentalHealthModel(preprocessing_object=preprocessing_obj,
                                                    trained_model_object=best_model_detail.best_model)
            logging.info("Created Mental health model object with preprocessor and model")
            logging.info("Created best model file path")
            
            save_object(self.model_trainer_config.trained_model_file_path, mental_health_model)
            
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                metric_artifact=metric_artifact
            )
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")
            
            return model_trainer_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)