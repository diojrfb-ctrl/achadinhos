#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build..."

# Instala dependências Python
pip install -r requirements.txt

# Limpa cache antigo (opcional, mas pode ajudar)
rm -rf /opt/render/.cache/ms-playwright/* 2>/dev/null || true

# Instala o Chromium com todas as dependências
echo "📥 Instalando Chromium..."
python -m playwright install chromium
python -m playwright install-deps chromium

# Verifica a instalação
echo "🔍 Verificando instalação..."
CACHE_DIR="/opt/render/.cache/ms-playwright"

if [ -d "$CACHE_DIR" ]; then
    echo "✅ Playwright cache encontrado"
    ls -la "$CACHE_DIR"
    
    # Mostra detalhes da versão 1208 especificamente
    if [ -d "$CACHE_DIR/chromium_headless_shell-1208" ]; then
        echo "✅ Versão 1208 encontrada!"
        ls -la "$CACHE_DIR/chromium_headless_shell-1208/"*
    else
        echo "⚠️ Versão 1208 não encontrada. Pastas disponíveis:"
        ls -d "$CACHE_DIR"/* 2>/dev/null | grep -o '[^/]*$' || true
    fi
else
    echo "❌ Cache não encontrado em $CACHE_DIR"
fi

echo "✅ Build concluído!"