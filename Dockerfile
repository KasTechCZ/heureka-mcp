FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .

RUN pip install uv

# Move virtual environment outside /app to prevent it from being overwritten by volume mounts
ENV UV_PROJECT_ENVIRONMENT=/venv

# Sync dependencies to the custom environment location
RUN uv sync --frozen --extra test

COPY . .

# Ensure the venv is in PATH
ENV PATH="/venv/bin:$PATH"

CMD ["uv", "run", "main.py"]
