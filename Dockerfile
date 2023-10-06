FROM python:3.10

WORKDIR /scripts

COPY /scripts .
COPY requirements.txt /scripts/requirements.txt

RUN pip install -r requirements.txt

CMD if [ "$DEBUG" = "1" ]; then \
        python -m debugpy --wait-for-client --listen 0.0.0.0:5678 -m server run --host=0.0.0.0; \
    else \
        python server.py; \
    fi