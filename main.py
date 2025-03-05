from Network_Security.Components.data_ingestion import DataIngestion
from Network_Security.Components.data_validation import DataValidation
from Network_Security.Components.data_transformation import DataTransformation
from Network_Security.Components.model_trainer import ModelTrainer

from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging

from Network_Security.Entity.config_entity import (
    DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig, 
    DataTransformationConfig, ModelTrainerConfig
)

import sys

if __name__ == "__main__":
    try: 
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Starting Data Ingestion process...") 
        
        data_ingestion_artifacts = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifacts)

        logging.info("Data Ingestion Completed")

        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifacts, data_validation_config)

        logging.info("Starting Data Validation process...") 

        data_validation_artifacts = data_validation.initiate_data_validation()
        print(data_validation_artifacts)

        logging.info("Data Validation Completed")

        data_transformation_config=DataTransformationConfig(training_pipeline_config)

        logging.info("Started Data Transformation process...")
        
        data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config)
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        
        print(data_transformation_artifact)
        
        logging.info("Data Transformation completed")

        logging.info("Model Training stared...")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(model_trainer_config=model_trainer_config,data_transformation_artifact=data_transformation_artifact)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Training artifact created")

    except Exception as e:
        raise NetworkSecurityException(e, sys)