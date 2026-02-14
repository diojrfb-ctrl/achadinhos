import os
import glob
from playwright.async_api import async_playwright

async def obter_browser():
    """Busca recursivamente por qualquer executável do Chromium no Render."""
    pw = await async_playwright().start()
    
    # Lista de padrões para encontrar o executável, não importa a versão
    padrões = [
        "/opt/render/.cache/ms-playwright/**/chrome",
        "/opt/render/.cache/ms-playwright/**/chrome-headless-shell",
        "/home/render/.cache/ms-playwright/**/chrome",
        "/home/render/.cache/ms-playwright/**/chrome-headless-shell"
    ]
    
    executable = None
    for pattern in padrões:
        found = glob.glob(pattern, recursive=True)
        # Filtra para garantir que pegamos o arquivo executável real
        for path in found:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                executable = path
                break
        if executable: break

    print(f"DEBUG: Binário encontrado em: {executable}")
    
    browser = await pw.chromium.launch(
        headless=True,
        executable_path=executable, # Se for None, o Playwright tenta o padrão
        args=["--no-sandbox", "--disable-dev-shm-usage"]
    )
    
    context = await browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    )
    
    return pw, browser, context