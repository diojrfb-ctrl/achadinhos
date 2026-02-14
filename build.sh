#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build..."

# Instala dependências Python
pip install -r requirements.txt

# Instala o Chromium com todas as dependências
echo "📥 Instalando Chromium..."
python -m playwright install chromium --with-deps

# Verifica onde foi instalado
echo "🔍 Verificando instalação..."
CACHE_DIR="/opt/render/.cache/ms-playwright"
if [ -d "$CACHE_DIR" ]; then
    echo "✅ Playwright cache encontrado em: $CACHE_DIR"
    ls -la "$CACHE_DIR"
    
    # Procura pelo executável do chrome
    CHROME_PATH=$(find "$CACHE_DIR" -name "chrome" -type f | head -1)
    if [ -n "$CHROME_PATH" ]; then
        echo "✅ Chromium executável encontrado em: $CHROME_PATH"
    else
        echo "❌ Chromium executável não encontrado!"
    fi
else
    echo "❌ Cache directory não encontrado: $CACHE_DIR"
    
    # Tenta encontrar em outros locais
    echo "🔍 Procurando em outros locais..."
    find / -name "chrome" -type f 2>/dev/null | grep -E "(playwright|chromium)" | head -5 || true
fi

echo "✅ Build concluído!"