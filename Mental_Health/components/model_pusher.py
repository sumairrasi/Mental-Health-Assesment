import sys
from Mental_Health.cloud_storage.aws_storage import SimpleStorageService
from Mental_Health.exception import MentalHealthException
from Mental_Health.logger import logging
from Mental_Health.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from Mental_Health.entity.config_entity import ModelPusherConfig
from Mental_Health.entity.s3_estimator import MentalHealthEstimator




class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.mentalhealth_estimator = MentalHealthEstimator(bucket_name=model_pusher_config.bucket_name,
                                                            model_path=model_pusher_config.s3_model_key_path)
        
        
    def initiate_model_pusher(self) -> ModelPusherArtifact:
        logging.info(f"Entered initiate model pusher")
        try:
            logging.info("uploading artifacts folders to s3 bucket")
            self.mentalhealth_estimator.save_model(from_file=self.model_evaluation_artifact.trained_model_path)
            model_pusher_artifact = ModelPusherArtifact(bucket_name=self.model_pusher_config.bucket_name,
                                                        s3_model_path=self.model_pusher_config.s3_model_key_path)
            logging.info("Uploaded artifacts folder to s3 bucket")
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate model pusher method of ModelTrainer class")
            return model_pusher_artifact
        except Exception as e:
            raise MentalHealthException(e,sys)