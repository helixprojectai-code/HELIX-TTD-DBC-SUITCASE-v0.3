# HELIX-TTD CONTAINER NODE
# Status: LIGHTWEIGHT // ALPINE
FROM python@sha256:c825a02ff096b3dc3d362015f9e9f6527f66b73e11f9ad2db1f0da4e09ba7030
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
