# HELIX-TTD CONTAINER NODE
# Status: LIGHTWEIGHT // ALPINE
FROM python:3.11-alpine

WORKDIR /app

# Install build deps for cryptography (if needed on Alpine)
RUN apk add --no-cache gcc musl-dev libffi-dev openssl-dev

# Copy manifest
COPY . .

# Install Helix Logic
RUN pip install --no-cache-dir .

# Default Entrypoint: The Helix CLI
ENTRYPOINT ["helix"]

# Default Command (Help)
CMD ["--help"]
