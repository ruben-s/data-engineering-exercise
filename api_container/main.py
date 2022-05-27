from flask import Flask, request, Response
import json
import numpy as np


app=Flask(__name__)

#we are importing our prediction function from the prediction.py file
from prediction import car_price_prediction

dict_keys = ('vehicletype','gearbox','powerps','model','km','regmonth','fueltype','brandid')

general_error_msg = ('''Input to estimate should be provided as json to parameter 'prediction_input'. ''' +
                    'Example of expected json:' +
                    ''' '{'vehicletype':'-1','gearbox':'1','powerps':'0','model':'118','km':'150000','regmonth':'0', ''' +
                    ''' 'fueltype':'1','brandid':'38'} ''' +
                    '''Note: json should be url encoded''' )

def validate_and_format_input(input_to_validate) -> dict:
    """ Validate the input by checking if all required keys are present.
        Return a dict with both 2D array of validated input and empty error,
        or empty validated error and an error message.
    """
    validated_and_formated_input = []
    error = ''
    # try to convert the serialized json back to json
    try:
        input_dict = json.loads(input_to_validate)
    except Exception as e:
        error = str(e)

    # validate the provided json to have all the keys
    validated_input_list = []
    for key in dict_keys:
        if input_dict.get(key):
            validated_input_list.append(input_dict.get(key))    
        else:
            error= 'The ' + str(key)+ ' parameter is not provided. '
            break
    
    # out of the validated list of parameters create a 2D array
    validated_and_formated_input = np.array(validated_input_list)
    validated_and_formated_input = validated_and_formated_input.reshape(1,-1)

    return {"validated_input":validated_and_formated_input, "error": error}

@app.route("/",methods=['GET','POST'])
def index():
    resp = Response()
    if request.method=='GET':
        prediction_input = request.args.get('prediction_input')
        result_dict = validate_and_format_input(prediction_input)
        if result_dict.get('error'):
            # return jsonify(result_dict.get('error'))
            # return result_dict.get('error')
            response_data = {'error' : str(result_dict.get('error')) + general_error_msg}
            # resp = Response(result_dict.get('error'), mimetype='application/json')
            resp.status_code = 400
        else:
            validated_prediction_input = result_dict.get('validated_input')
            try:
                predicted_value = car_price_prediction(validated_prediction_input)
            except Exception as e:
                response_data = {'error' : str(e) + general_error_msg}
                resp.status_code = 400
                # return jsonify( str(e) + general_error_msg)
            response_data = { 'estimated_value': str(predicted_value)}    
            resp.status_code = 200
            # return jsonify( estimated_value = str(predicted_value)), status_code
            # return resp
    else:
        # return jsonify({'Error':"This is a GET API method"})
        response_data = { 'error':"This is a GET API method" }
        resp.status_code = 400

    resp = Response(json.dumps(response_data), mimetype='application/json')
    return resp

if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0', port=9007)
    app.run(debug=False,host='0.0.0.0', port=9007)