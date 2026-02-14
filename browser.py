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
    # User-Agent real para evitar Captcha da Amazon
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")
    
    # Localizar o binário do Chromium do Playwright no Render (Caminho de Usuário)
    path_pattern = "/home/render/.cache/ms-playwright/chromium-*/chrome-linux/chrome"
    found_paths = glob.glob(path_pattern)
    
    if found_paths:
        chrome_options.binary_location = found_paths[0]
        print(f"✅ Navegador Playwright detectado: {found_paths[0]}")
    else:
        # Se falhar, tenta o caminho padrão (fallback)
        if os.path.exists("/usr/bin/google-chrome"):
            chrome_options.binary_location = "/usr/bin/google-chrome"
        print("⚠️ Usando caminho padrão do sistema")

    # Instala o driver compatível
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)