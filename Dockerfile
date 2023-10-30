FROM python:3.11
RUN apt-get update && apt-get install -y nano

WORKDIR /app

COPY components ./components
COPY notebooks ./notebooks
COPY ontology ./ontology
COPY README.md .
COPY requirements.txt .

RUN pip install -r requirements.txt
RUN mkdir credentials/openai_key.txt

EXPOSE 8501 
