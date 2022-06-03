from flask import Flask, request, Response
import json
import numpy as np
#we are importing our prediction class from the prediction.py file
from prediction import CarCostEstimator

app=Flask(__name__)

# instantiate the CarCostEstimator to load the model at Flask start-up
app.CarPricePredictor = CarCostEstimator("../lgbr_cars.model")

general_error_msg = ('''Input for prediction should be provided as json to urlparameter 'prediction_input'. ''' +
                    ''' Note that all inputs are integer numbers.''' +
                    'Example of expected json:' +
                    ''' '{'vehicletype':'-1','gearbox':'1','powerps':'0','model':'118','km':'150000','regmonth':'0', ''' +
                    ''' 'fueltype':'1','brandid':'38'} ''' +
                    '''Note: json should be url encoded''' )

def validate_and_format_input(input_to_validate) -> dict:
    """ Validate the input by checking if all required keys are present.
        Return a dict with both 2D array of validated input and empty error,
        or empty validated error and an error message.
    """
    model_parameters_tuple = app.CarPricePredictor.get_model_parameters()

    validated_and_formated_input = []
    error = ''
    # try to convert the serialized json back to json
    if (input_to_validate is None) or (not input_to_validate.strip('\"')):
        error = 'There was no input provided. '
    else:
        try:
            input_dict = json.loads(input_to_validate)
        except Exception as e:
            error = str(e)
        # validate the provided json to have all the keys
        validated_input_list = []
        for key in model_parameters_tuple:
            if input_dict.get(key):
                validated_input_list.append(int(input_dict.get(key)))    
            else:
                error= 'The ' + str(key)+ ' parameter is not provided. '
                break
    
        # out of the validated list of parameters create a 2D array
        validated_and_formated_input = np.array(validated_input_list)
        validated_and_formated_input = validated_and_formated_input.reshape(1,-1)

    return {"validated_input":validated_and_formated_input, "error": error}

@app.route("/",methods=['GET','POST'])
def index():
    # create empty response to be completed depending on outcome of prediction
    resp = Response()
    predicted_value = 0.0
    prediction_input = ''
    response_data = {'error' : 'Did not seem to get any input!' + general_error_msg}
    resp.status_code = 400
    if request.method=='GET':           
        prediction_input = request.args.get('prediction_input')
        result_dict = validate_and_format_input(prediction_input)
        # if an error is found in the validation of the input then set response accordingly
        if result_dict.get('error'):
            response_data = {'error' : str(result_dict.get('error')) + general_error_msg}
            resp.status_code = 400
        # no error so input seems ok
        else:
            validated_prediction_input = result_dict.get('validated_input')
            try:
                predicted_value = app.CarPricePredictor.car_price_prediction(validated_prediction_input)
            except Exception as e:
                response_data = {'error' : str(e) + general_error_msg}
                resp.status_code = 400
            response_data = { 'estimated_value': str(predicted_value)}    
            resp.status_code = 200
    else:
        response_data = { 'error':"This is a GET API method" }
        resp.status_code = 400
    # fill the response object with the actual prediction in json format
    resp = Response(json.dumps(response_data), mimetype='application/json')
    return resp

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0', port=9007)
    app.run(debug=False,host='0.0.0.0', port=9007)