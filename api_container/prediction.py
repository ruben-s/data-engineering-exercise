import joblib
import lightgbm as lgb
import numpy as np

class CarCostEstimator():
    ''' Class implementing the prediction of a car price based on the input parameters given.


    Class will load the trained model on initialisation.
    '''
    model_parameters_tuple = ('vehicletype','gearbox','powerps','model','km','regmonth','fueltype','brandid')

   
    lgbr_cars = lgb.LGBMModel()

    def __init__(self, path: str) -> None:
        try:
            file_handle = open(path,'rb')
        except IOError as e:
            raise(e)
        print('created new CarCostEstimator with loaded model')
        self.lgbr_cars = joblib.load(file_handle)

    def get_model_parameters(self) -> tuple:
        return self.model_parameters_tuple

    def car_price_prediction(self, single_input) -> float:
        predicted_value = self.lgbr_cars.predict(single_input)
        # predicted_value is of type numpy.ndarray with a single element
        # get the float out
        predicted_value_float = round(float(predicted_value.item()),3)
        return predicted_value_float

# allow testing of the module independently
if __name__ == '__main__':
    CarCostPredictor = CarCostEstimator("../lgbr_cars.model")
    model_test_input = [[3,1,190,-1,125000,5,3,1]]
    predicted_value = CarCostPredictor.car_price_prediction(model_test_input)
    print(predicted_value)