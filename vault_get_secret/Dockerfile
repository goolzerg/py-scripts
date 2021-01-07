FROM python:rc-alpine3.12

COPY ./vault.py /vault.py

RUN pip install --no-cache-dir hvac && \
touch /service_variables.env

ENTRYPOINT ["python3", "/vault.py"]
