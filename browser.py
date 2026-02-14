import os
import glob
from playwright.async_api import async_playwright

async def obter_browser():
    """Inicia o motor Playwright de forma compatível com o Render."""
    pw = await async_playwright().start()
    
    # Busca o executável do Chromium no diretório de usuário do Render
    path_pattern = "/home/render/.cache/ms-playwright/chromium-*/chrome-linux/chrome"
    found_paths = glob.glob(path_pattern)
    executable = found_paths[0] if found_paths else None
    
    browser = await pw.chromium.launch(
        headless=True,
        executable_path=executable,
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    
    return pw, browser, context