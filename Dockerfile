FROM python:3.6

WORKDIR /griffier
COPY . /griffier

RUN python3.6 -m pip install -r requirements.txt

CMD bash deploy.sh
