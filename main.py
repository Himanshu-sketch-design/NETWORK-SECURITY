from Network_Security.Components.data_ingestion import DataIngestion
from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging
from Network_Security.Entity.config_entity import (
    DataIngestionConfig, TrainingPipelineConfig
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

    except Exception as e:
        raise NetworkSecurityException(e, sys)