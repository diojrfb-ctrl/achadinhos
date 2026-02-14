import os
import subprocess
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright forçando o caminho local para evitar erros de 
    binário inexistente no Render.
    """
    # Define onde os navegadores devem estar (dentro da pasta do projeto)
    os.environ["PLAYWRIGHT_BROWSERS_PATH"] = os.path.join(os.getcwd(), ".playwright")
    
    pw = await async_playwright().start()
    
    try:
        # Tentativa de lançar o navegador
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox", 
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        return pw, browser, context
        
    except Exception as e:
        await pw.stop()
        print(f"ERRO CRÍTICO no browser.py: {e}")
        raise e