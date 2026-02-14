#!/usr/bin/env bash
# Sair em caso de erro
set -o errexit

# Instala as dependências do Python
pip install -r requirements.txt

# Instala o Playwright e os navegadores necessários
playwright install chromium