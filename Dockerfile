FROM python:3.6

WORKDIR /griffier
COPY . /griffier

RUN python3.6 -m pip install -r requirements.txt

CMD python3.6 -u griffier.py
