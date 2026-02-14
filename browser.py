import os
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright otimizado para ambientes sem root (Render).
    """
    pw = await async_playwright().start()
    
    try:
        # Lançamos o chromium com flags que desativam recursos que exigem
        # bibliotecas de sistema que podem estar faltando.
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--no-zygote",
                "--single-process",
                "--disable-extensions"
            ]
        )
        
        # O User-Agent é essencial para não ser bloqueado pela Amazon
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        
        return pw, browser, context
        
    except Exception as e:
        await pw.stop()
        print(f"❌ Erro ao iniciar browser: {e}")
        raise e