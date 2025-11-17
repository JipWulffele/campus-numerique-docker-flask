FROM python:3.12-slim

# Install uv
RUN pip install uv

# Install dependencies
WORKDIR /mini_project
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy working directory into docker image
COPY . .

CMD ["uv", "run", "app.py", "--host=0.0.0.0"]
