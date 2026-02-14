import os
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright otimizado para o ambiente Render.
    """
    pw = await async_playwright().start()
    
    try:
        # Forçamos flags que desativam a necessidade de sandbox e GPU, 
        # essenciais para rodar em containers.
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-setuid-sandbox",
                "--no-zygote"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        )
        
        return pw, browser, context
        
    except Exception as e:
        if pw:
            await pw.stop()
        print(f"❌ Erro ao iniciar browser: {e}")
        raise e