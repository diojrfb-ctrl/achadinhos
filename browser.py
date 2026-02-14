import os
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright otimizado para ambientes restritos (Render).
    """
    pw = await async_playwright().start()
    
    try:
        # Lançamos o chromium com flags para evitar necessidade de root e GPU
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--disable-gpu",
                "--no-zygote",
                "--single-process"
            ]
        )
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        
        return pw, browser, context
        
    except Exception as e:
        await pw.stop()
        print(f"❌ Erro ao iniciar browser: {e}")
        raise e