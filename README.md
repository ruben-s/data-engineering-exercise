# data-engineering-exercise
Data engineering home exercise

## Set-up the environment for the notebook

1.  clone the git repo

        git clone https://github.com/ruben-s/data-engineering-exercise.git

1.  create the virtual environment inside the cloned project directory

        python3 -m venv [environment name]

    Note: environment name used here is py3_dsclp and was added to .gitignore

1.  Activate the virtual environment

        source ./py3_dsclp/bin/activate

1.  Upgrade pip

        python -m pip install --upgrade pip

1.  Install pip-tools (cfr to [Pip tools on Github](https://github.com/jazzband/pip-tools))

        python -m pip install pip-tools

1.  Install the dependencies by use of pip-sync

        pip-sync

    Note: to upgrade/recalculate the requirements.txt use pip-compile --upgrade

1. start the Jupyter Lab environment

        jupyter-lab


## Run the docker container for serving the Rest API with the car price model prediction

Note: It is assumed that a functional docker environment exists and curl is installed

Reference: (https://predictivehacks.com/how-to-use-docker-for-flask-api/)


1.  build the docker container based on the docker file

        docker build -t api_car_price_prediction -f ./api_container/Dockerfile .

1.  start the docker container
    Note: the 9007 tcp port exposed by the container is mapped to 5000 on the localhost

        docker run -d -p 5000:9007 api_car_price_prediction

1.  Get a prediction value

    Note:  
    The input parameters are passed as a json, but URL encoded  
    So {"vehicletype":"-1","gearbox":"1","powerps":"0","model":"118","km":"150000","regmonth":"0","fueltype":"1","brandid":"38"} 

    Becomes -> %7B'vehicletype'%3A'-1'%2C'gearbox'%3A'1'%2C'powerps'%3A'0'%2C'model'%3A'118'%2C'km'%3A'150000'%2C'regmonth'%3A'0'%2C'fueltype'%3A'1'%2C'brandid'%3A'38'%7D  

        curl -G "http://localhost:5000/" -d 'prediction_input=%7B%22vehicletype%22%3A%22-1%22%2C%22gearbox%22%3A%221%22%2C%22powerps%22%3A%220%22%2C%22model%22%3A%22118%22%2C%22km%22%3A%22150000%22%2C%22regmonth%22%3A%220%22%2C%22fueltype%22%3A%221%22%2C%22brandid%22%3A%2238%22%7D'

1.  stop the docker image

    get the container_id first   

        docker ps

    stop the container   

        docker stop [container_id]

1. remove the docker container

        docker rm [container_id]

## Prepare the environment for GIS

On Ubuntu some OS dependencies need to be installed  
Note: this is done on an Ubuntu 18.04 Mate system

**Note: It appears that GDAL is not needed in the end?**
To be verified with more experience & testing!

1.  Install GDAL

    cfr (https://stackoverflow.com/questions/37294127/python-gdal-2-1-installation-on-ubuntu-16-04/41613466#41613466)

        sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
        sudo apt-get update
        sudo apt-get install gdal-bin python-gdal python3-gdal
        sudo apt-get install libgdal-dev

1.  Get version of installed gdal

        gdalinfo --version

1.  Add the correct version to requirements.in

1.  Recompile requirements.txt

        pip-compile

1.  Install required dependencies

        pip-sync
    

