import os
import glob
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def configurar_navegador():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # Busca o binário do Chromium instalado pelo Playwright no Render
    if os.getenv("RENDER"):
        # O asterisco ajuda a ignorar a variação da versão (ex: chromium-1155)
        path_pattern = "/home/render/.cache/ms-playwright/chromium-*/chrome-linux/chrome"
        found_paths = glob.glob(path_pattern)
        
        if found_paths:
            chrome_options.binary_location = found_paths[0]
            print(f"✅ Navegador encontrado: {found_paths[0]}")
        else:
            # Tenta um caminho alternativo comum em instâncias Linux
            chrome_options.binary_location = "/usr/bin/google-chrome"
            print("⚠️ Usando caminho padrão do sistema para o Chrome")

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)