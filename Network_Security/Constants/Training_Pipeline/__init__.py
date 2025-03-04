import os
import sys
import numpy as np
import pandas as pd

"""
Defining common constant variables for training pipeline
"""

TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "Network_Security"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"
DATA_FILE: str = "HIMANSHU_AI"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

"""
Data Ingetsion related constant start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "Network_Data"
DATA_INGESTION_DATABASE_NAME: str = "HIMANSHU_AI.db"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2
JSON_FILE_PATH = "HIMANSHU_AI.json"