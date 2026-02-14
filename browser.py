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
    
    # No Render, tentamos encontrar o Chromium do Playwright
    if os.getenv("RENDER"):
        try:
            # Comando que retorna onde o executável foi instalado
            executable_path = subprocess.getoutput("which chromium").strip()
            if not executable_path:
                # Caminho padrão do Playwright no Linux
                executable_path = "/home/render/.cache/ms-playwright/chromium-1155/chrome-linux/chrome"
            chrome_options.binary_location = executable_path
        except:
            pass

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)