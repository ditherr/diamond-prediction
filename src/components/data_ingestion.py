import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.transform_training import *

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join('artifact', 'data.csv')
    train_data_path: str = os.path.join('artifact', 'train.csv')
    test_data_path: str = os.path.join('artifact', 'test.csv')
    

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        
    def initiate_data_ingestion(self):        
        logging.info("Entered the data ingestion method or component") 
        try:
            data = pd.read_csv('data/diamonds.csv') # read the dataset as dataframe
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True) # make directory for the artifacts
            data.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) # save the train data
            
            # logging.info("Train Test Split initiated")
            train_set, test_set = train_test_split(data, test_size=0.2, random_state=42) # train and split the data
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) # save the train data
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) # save the test data
            
            # logging.info("Ingestion of data is completed")
            
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:
            raise CustomException(e, sys)