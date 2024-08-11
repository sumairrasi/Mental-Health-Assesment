from dataclasses import dataclass
import os

@dataclass
class DataIngestionArtifact:
    training_file_path:str
    testing_file_path:str
    


@dataclass
class DataValidationArtifact:
    validation_status: bool
    message: str
    drift_report_file_path: str