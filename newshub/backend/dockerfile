# backend/Dockerfile

FROM python:3.12-slim

# Define o diretório de trabalho principal
WORKDIR /app

# Copia apenas o arquivo de dependências
COPY ./requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para um subdiretório 'src'
COPY ./app /app/src

# Define o novo diretório de trabalho para o Gunicorn
WORKDIR /app/src

# Expõe a porta que o Gunicorn irá usar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]