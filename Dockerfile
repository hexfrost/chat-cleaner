FROM python:3.10.6

WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install


CMD ["uvicorn", "tg_cleaner:app", "--workers", "1", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 80
