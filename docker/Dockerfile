# ==========================================
# STAGE 1: BUILDER (Compilação e Dependências)
# ==========================================
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /build

# Isolamento de dependências via Virtual Environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# ==========================================
# STAGE 2: RUNNER (Ambiente de Execução Seguro)
# ==========================================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Criação de usuário não-privilegiado sob a taxonomia Secure by Design
RUN groupadd -g 1000 smartfarm && \
    useradd -u 1000 -g smartfarm -s /bin/bash -m smartfarm

WORKDIR /app

# Injeção exclusiva do ambiente virtual compilado
COPY --from=builder /opt/venv /opt/venv

# Transferência do código-fonte com atribuição rigorosa de propriedade
COPY --chown=smartfarm:smartfarm src/backend/ /app/

# Bloqueio de execução como root
USER smartfarm
