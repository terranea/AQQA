FROM python:3.11
RUN apt-get update && apt-get install -y nano

WORKDIR /app

ADD components /components
ADD notebooks /notebooks
ADD ontology /ontology
COPY README.md .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8501 
