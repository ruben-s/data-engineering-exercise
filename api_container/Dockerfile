FROM python:3.6

COPY ./api_container/requirements.txt ./requirements.txt
COPY ./api_container/prediction.py ./prediction.py
COPY ./api_container/main.py ./main.py
COPY ./lgbr_cars.model ./lgbr_cars.model

RUN python -m pip install --upgrade pip
RUN pip install pip-tools
RUN pip-sync

CMD ["python", "./main.py"]