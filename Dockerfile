FROM python:3.11
RUN apt-get update && apt-get install -y nano

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY components ./components
COPY notebooks ./notebooks
COPY ontology ./ontology
COPY README.md .

RUN mkdir credentials

EXPOSE 8501 
