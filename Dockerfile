# HELIX-TTD CONTAINER NODE
# Status: HERMETIC // PINNED // ROOTLESS
# -----------------------------------------------------------------------------
# SECURITY NOTE: Replace the SHA256 below with the output from Step 1.
# This ensures your build is immutable and immune to tag hijacking.
# -----------------------------------------------------------------------------
FROM python@sha256:REPLACE_WITH_ACTUAL_SHA256_FROM_STEP_1

# Metadata for SBOM scanners (Syft/Grype)
LABEL org.opencontainers.image.title="HELIX-TTD Identity Node"
LABEL org.opencontainers.image.description="Sovereign Identity & Custody Provider"
LABEL org.opencontainers.image.source="https://github.com/helixprojectai-code/HELIX-TTD-DBC-SUITCASE-v0.3"
LABEL org.opencontainers.image.licenses="Apache-2.0"

WORKDIR /app

# 1. SECURITY: Create a non-root user (UID 1000)
# We do this first so we own the directory but drop privs later
RUN addgroup -S helix && adduser -S helix -G helix

# 2. INSTALL: Build dependencies for Cryptography (Ed25519)
# Alpine requires these for compiling C-extensions
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    openssl-dev \
    git

# 3. COPY: Transfer the sovereign code
# We copy everything, then install
COPY . .

# 4. BUILD: Install the package
# --no-cache-dir keeps the image slim and removes temp build artifacts
RUN pip install --no-cache-dir .

# 5. SECURITY: Drop Root Privileges
# From this point forward, the container cannot modify system files
USER helix

# 6. RUNTIME: Define the Entrypoint
# Default command shows help; arguments can be passed via docker run
ENTRYPOINT ["helix"]
CMD ["--help"]
