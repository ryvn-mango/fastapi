# Use Python 3.12 slim image as base
FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Create virtual environment
RUN uv venv
ENV VIRTUAL_ENV=/app/.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy dependency files for better layer caching
COPY pyproject.toml ./

# Install dependencies using uv
RUN uv pip install .

# Copy the application code
COPY ./app ./app

EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 