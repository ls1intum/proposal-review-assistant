FROM python:3.13-alpine

RUN apk update && \
    apk add --no-cache gcc g++ make musl-dev postgresql-dev rust cargo curl clang

RUN pip install poetry==2.1.1

WORKDIR /app

# Copy proposal-review-assistant files
COPY pyproject.toml poetry.lock /app/proposal-review-assistant/
COPY app/ /app/proposal-review-assistant/app/

# Set working directory to proposal-review-assistant folder where the poetry config is
WORKDIR /app/proposal-review-assistant

# Install dependencies
RUN poetry install --no-root

# Run the app
CMD ["poetry", "run", "app"]