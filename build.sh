#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build..."

# Instala dependências Python
pip install -r requirements.txt

# Instala o Chromium e dependências do sistema
python -m playwright install chromium
python -m playwright install-deps chromium

# Cria diretório de cache e dá permissões
mkdir -p /opt/render/.cache/ms-playwright
chmod -R 777 /opt/render/.cache

# Log do caminho do executável
echo "🔍 Verificando instalação do Chromium..."
find /opt/render/.cache/ms-playwright -name "chrome" -type f 2>/dev/null || echo "Chrome não encontrado em /opt/render"
find ~/.cache/ms-playwright -name "chrome" -type f 2>/dev/null || echo "Chrome não encontrado em ~/.cache"

echo "✅ Build concluído!"