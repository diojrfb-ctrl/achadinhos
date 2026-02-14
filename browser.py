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
    
    # Busca automática do binário do Chromium no Render
    if os.getenv("RENDER"):
        # O Playwright instala em ~/.cache/ms-playwright/chromium-<numero>/chrome-linux/chrome
        base_path = "/home/render/.cache/ms-playwright/chromium-*"
        binarios = glob.glob(os.path.join(base_path, "chrome-linux/chrome"))
        
        if binarios:
            chrome_options.binary_location = binarios[0]
            print(f"✅ Chromium encontrado em: {binarios[0]}")
        else:
            print("⚠️ Chromium não encontrado pelo glob, tentando caminho alternativo...")
            chrome_options.binary_location = "/usr/bin/google-chrome"

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)