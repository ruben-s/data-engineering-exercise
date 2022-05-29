import joblib
import lightgbm as lgb
import numpy as np

def retrieve_model(path):
    try:
        file_handle = open(path,'rb')
    except IOError as e:
        raise(e)
    trained_model = joblib.load(file_handle)
    return trained_model

def car_price_prediction(single_input) -> float:
    lgbr_cars = retrieve_model("../lgbr_cars.model")
    predicted_value = lgbr_cars.predict(single_input)

    # predicted_value is of type numpy.ndarray with a single element
    # get the float out
    predicted_value_float = round(predicted_value.item(),3)
    return predicted_value_float

# allow testing of the module independently
if __name__ == '__main__':
    model_test_input = [[3,1,190,-1,125000,5,3,1]]
    predicted_value = car_price_prediction(model_test_input)
    print(predicted_value)