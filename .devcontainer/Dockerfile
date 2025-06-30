FROM mcr.microsoft.com/devcontainers/python:3.11

RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get update && \
    apt-get install -y nodejs docker.io && \
    rm -rf /var/lib/apt/lists/*

RUN npm install -g @google/gemini-cli --unsafe-perm

