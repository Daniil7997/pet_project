FROM python:3.11.4-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app/pet_project
CMD ["python", "manage.py", "runserver"]

# CMD ["sleep", "infinity"] ничего не делает и держит контейнер запущенным.
# CMD ["python", "manage.py", "runserver"]   ---- прежний вариант
# рекомендуется использовать аргументы JSON для CMD