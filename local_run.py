from src.components.data_ingestion import DataIngestion
from src.components.transform_training import ModelDevelopment


if __name__ == "__main__":
    # Apply Data Ingestion
    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion() ## train and test .csv
    
    # Applying Transformation process into train and test data (ingestion result)
    data_transformation = ModelDevelopment()
    data_transformation.transform_train(train_data, test_data)