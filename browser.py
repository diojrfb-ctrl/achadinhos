import os
import glob
from playwright.async_api import async_playwright

async def obter_browser():
    """Localiza o executável do Playwright em qualquer diretório do Render."""
    pw = await async_playwright().start()
    
    # Lista de caminhos possíveis onde o Render pode instalar o browser
    caminhos_possiveis = [
        "/opt/render/.cache/ms-playwright/chromium-*/chrome-linux/chrome",
        "/home/render/.cache/ms-playwright/chromium-*/chrome-linux/chrome",
        "/opt/render/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell"
    ]
    
    executable = None
    for pattern in caminhos_possiveis:
        found = glob.glob(pattern)
        if found:
            executable = found[0]
            break
    
    # Se executable for None, o Playwright tentará usar o padrão do sistema
    browser = await pw.chromium.launch(
        headless=True,
        executable_path=executable,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    
    return pw, browser, context