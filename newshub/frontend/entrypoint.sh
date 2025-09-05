#!/bin/sh

# Garante que o usuário 'node' seja o proprietário do diretório node_modules.
# O comando 'su-exec' é usado para executar um comando como um usuário específico.
# É mais seguro e leve que 'sudo'.
su-exec node chown -R node:node /app/node_modules

# Executa o comando principal do contêiner (o CMD do Dockerfile)
exec "$@"