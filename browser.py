import os
import subprocess
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
    
    # Tenta localizar o executável do Chromium instalado pelo Playwright
    try:
        import playwright
        # Comando para pegar o caminho do executável
        path = subprocess.check_output(["playwright", "wk", "path"]).decode().strip()
        # Nota: No Render, o caminho geralmente fica em /home/render/.cache/ms-playwright/
        chrome_options.binary_location = path
    except:
        pass

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)