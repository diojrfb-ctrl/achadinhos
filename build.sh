#!/usr/bin/env bash
set -o errexit

echo "🚀 Iniciando build do OfertasFlashBR"
echo "===================================="

# Instala dependências Python
echo "📦 Instalando dependências Python..."
pip install -r requirements.txt

# Instala o Playwright e browsers
echo "🎭 Instalando Playwright browsers..."
python -m playwright install chromium
python -m playwright install-deps chromium

# Verifica instalação
echo "🔍 Verificando instalação..."
CACHE_DIR="/opt/render/.cache/ms-playwright"

if [ -d "$CACHE_DIR" ]; then
    echo "✅ Playwright cache encontrado em: $CACHE_DIR"
    
    # Lista versões instaladas
    echo "📂 Versões do Chromium instaladas:"
    ls -la "$CACHE_DIR" | grep chromium || true
    
    # Procura pelo executável
    CHROME_PATH=$(find "$CACHE_DIR" -name "chrome" -o -name "chrome-headless-shell" -type f | head -1)
    if [ -n "$CHROME_PATH" ]; then
        echo "✅ Executável encontrado: $CHROME_PATH"
    else
        echo "⚠️ Executável não encontrado, mas deve funcionar em modo automático"
    fi
else
    echo "⚠️ Cache não encontrado em $CACHE_DIR"
fi

# Cria diretório para logs se necessário
mkdir -p logs

echo "✅ Build concluído com sucesso!"
echo "===================================="