# frontend/Dockerfile

# Usamos uma imagem oficial do Node.js (versão LTS Alpine para ser leve)
FROM node:24.7.0-alpine

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos de definição de dependências primeiro
COPY package*.json ./

# Instala as dependências como root
# Limpa o cache do npm para reduzir o tamanho da imagem
RUN npm ci && npm cache clean --force

# Copia o resto do código-fonte do frontend
COPY . .

# Cria o diretório de cache do Vite e define o usuário 'node' como proprietário.
# Isso permite que o processo do Vite, rodando como 'node', escreva neste diretório.
RUN mkdir -p /app/node_modules/.vite && chown -R node:node /app/node_modules/.vite

# Expõe a porta padrão do Vite
EXPOSE 5173

# Define o usuário para o comando principal, garantindo que o servidor
# não rode como root.
USER node

# Comando para iniciar o servidor de desenvolvimento
CMD ["npm", "run", "dev"]