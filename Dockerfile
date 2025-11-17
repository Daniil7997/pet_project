FROM python:3.11.4-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/pet_project
