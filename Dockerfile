# Dockerfile
FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Dependências do sistema (build de wheels e libs comuns)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Instala dependências Python
COPY requirements.txt .
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Porta padrão
EXPOSE 8000

# Sobe a API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
