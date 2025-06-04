FROM python:3.11-slim
WORKDIR /app
COPY pyproject.toml poetry.lock* /app/
RUN pip install poetry && poetry config virtualenvs.create false \
    && poetry install --no-dev
COPY . /app
CMD ["streamlit", "run", "src/streamlit_app.py", "--server.port", "8000", "--server.address", "0.0.0.0"]
