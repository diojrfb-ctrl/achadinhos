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
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Localizar o binário do Chromium do Playwright no Render
    path_pattern = "/home/render/.cache/ms-playwright/chromium-*/chrome-linux/chrome"
    found_paths = glob.glob(path_pattern)
    
    if found_paths:
        chrome_options.binary_location = found_paths[0]
        print(f"✅ Navegador Playwright detectado: {found_paths[0]}")
    else:
        # Se falhar, tenta o caminho padrão (fallback)
        chrome_options.binary_location = "/usr/bin/google-chrome"
        print("⚠️ Usando caminho padrão do sistema")

    # Instala o driver compatível
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)