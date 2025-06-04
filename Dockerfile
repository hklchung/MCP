FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry config virtualenvs.create false \
    && poetry install --no-dev
COPY . /app
ENV FLASK_APP=src.app
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
