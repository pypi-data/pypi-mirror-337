# Use an official Rust base image
FROM rust:1.85

# Install required dependencies for maturin and Python
RUN apt-get update && \
    apt-get install -y \
    python3-dev \
    python3-pip \
    python3-venv \
    libssl-dev \
    libpython3-dev \
    build-essential \
    libclang-dev \
    clang \
    curl \
    git \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install maturin
RUN which python3

# Create a virtual environment in /opt/venv

RUN pip install --break-system-packages setuptools wheel
RUN pip install --break-system-packages maturin

# Set up the working directory
WORKDIR /app

# Copy the PyO3 project into the container
COPY . .

CMD ["sleep", "infinity"]

# python3 -m build- maturin build for linux in the container