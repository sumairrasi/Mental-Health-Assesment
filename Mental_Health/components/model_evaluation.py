from Mental_Health.entity.config_entity import ModelEvaluationConfig
from Mental_Health.entity.artifact_entity import ModelTrainerArtifact,DataIngestionArtifact, ModelEvaluationArtifact
from sklearn.metrics import f1_score
from Mental_Health.exception import MentalHealthException
from Mental_Health.constants import TARGET_COLUMN, CURRENT_YEAR
from Mental_Health.logger import logging
import sys
import pandas as pd
from typing import Optional
from Mental_Health.entity.s3_estimator import MentalHealthEstimator
from dataclasses import dataclass
from Mental_Health.entity.estimator import TargetValueMapping


@dataclass
class EvaluationModelResponse:
    trained_model_f1_score: float
    best_model_f1_score: float
    is_model_accepted: bool
    difference: float
    

class ModelEvaluation:
    def __init__(self, model_eval_config: ModelEvaluationConfig, data_ingestion_artifact: DataIngestionArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            self.model_eval_config = model_eval_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.model_trainer_artifact = model_trainer_artifact
        except Exception as e:
            raise MentalHealthException(e, sys) from e
        
    def get_best_model(self) -> Optional[MentalHealthEstimator]:
        try:
            bucket_name = self.model_eval_config.bucket_name
            model_path = self.model_eval_config.s3_model_key_path
            mentalhealth_estimater =  MentalHealthEstimator(bucket_name=bucket_name,
                                                            model_path=model_path)
            if  mentalhealth_estimater.is_model_present(model_path=model_path):
                return mentalhealth_estimater
            return None

        except Exception as e:
            raise MentalHealthException(e, sys) from e
        
    
    def evaluate_model(self) -> EvaluationModelResponse:
        try:
            test_df = pd.read_csv(self.data_ingestion_artifact.testing_file_path)
            x, y = test_df.drop(TARGET_COLUMN, axis=1), test_df[TARGET_COLUMN]
            y = y.replace(
                TargetValueMapping()._asdict()
            )
            trained_model_f1_score = self.model_trainer_artifact.metric_artifact.f1_score
            best_model_f1_score = None
            best_model = self.get_best_model()
            if best_model is not None:
                y_hat_best_model = best_model.predict(x)
                best_model_f1_score = f1_score(y,y_hat_best_model)
            
            tmp_best_model_score = 0 if best_model_f1_score is None else best_model_f1_score
            result= EvaluationModelResponse(trained_model_f1_score=trained_model_f1_score,
                                            best_model_f1_score=best_model_f1_score,
                                            is_model_accepted=trained_model_f1_score > tmp_best_model_score,
                                            difference= trained_model_f1_score - tmp_best_model_score)
            logging.info(f"Result :{result}")
            return result
        except Exception as e:
            raise MentalHealthException(e,sys)
        
    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            evaluate_model_response = self.evaluate_model()
            s3_model_path = self.model_eval_config.s3_model_key_path
            model_evaluation_artifact = ModelEvaluationArtifact(
                is_model_accepted= evaluate_model_response.is_model_accepted,
                s3_model_path=s3_model_path,
                trained_model_path=self.model_trainer_artifact.trained_model_file_path,
                changed_accuracy=evaluate_model_response.difference   
            )
            logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
            return model_evaluation_artifact
        except Exception as e:
            raise MentalHealthException(e,sys) from e