FROM python:3.12-slim

WORKDIR /app

# Instalar dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código
COPY . .

# Expor a porta do Flask
EXPOSE 5000

# Rodar o servidor
CMD ["python", "search_engine.py"]