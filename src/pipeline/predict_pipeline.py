import os
import sys
import pandas as pd

from src.exception import CustomException
from src.logger import logging
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass
    
    # predict price
    def predict_price(self, features):
        try:
            model_path = os.path.join('data', 'final_model_pipeline.pkl')
            
            model = load_object(model_path)
            
            pred = model.predict(features)
            
            return pred
        
        except Exception as e:
            raise CustomException(e, sys)
        
    # predict carat
    def predict_carat(self, features):
        try:
            model_path = os.path.join('data', 'final_model_pipeline_carat.pkl')
            
            model = load_object(model_path)
            
            pred = model.predict(features)
            
            return pred
        
        except Exception as e:
            raise CustomException(e, sys)
    
    
## Responsible for mapping the input data
## Mapping all the inputs given in HTML to back-end
class CustomDataPrice:
    def __init__(self, carat: float, cut: str, color: str, clarity: str, 
                depth: float, table: float, x: float, y: float, z: float):
        
        self.carat = carat
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.depth = depth
        self.table = table
        self.x = x
        self.y = y
        self.z = z
    
    
    def get_data_price(self):
        try:
            dep_val = round(2 * self.z / (self.x + self.y), 3)*100
            
            custom_data_input_dict = {
                "carat": [self.carat],
                "cut": [self.cut],
                "color": [self.color],
                "clarity": [self.clarity],
                "depth": [dep_val],
                "table": [self.table],
                "x": [self.x],
                "y": [self.y],
                "z": [self.z],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)
        
        
    
class CustomDataCarat:
    def __init__(self, cut: str, color: str, clarity: str, depth: float, 
                    table: float, price: int, x: float, y: float, z: float):
    
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.depth = depth
        self.table = table
        self.price = price
        self.x = x
        self.y = y
        self.z = z
        
    def get_data_carat(self):
        try:
            dep_val = round(2 * self.z / (self.x + self.y), 3)*100
            
            custom_data_input_dict = {
                "cut": [self.cut],
                "color": [self.color],
                "clarity": [self.clarity],
                "depth": [dep_val],
                "table": [self.table],
                "price": [self.price],
                "x": [self.x],
                "y": [self.y],
                "z": [self.z],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)