import os
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright e o navegador Chromium.
    O Playwright buscará automaticamente o executável instalado no sistema.
    """
    # Inicia a instância do Playwright
    pw = await async_playwright().start()
    
    try:
        # Lançamento do navegador
        # 'executable_path' é omitido para que o Playwright use o padrão instalado via build script
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox", 
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--no-zygote",
                "--single-process" # Útil para economizar RAM em instâncias gratuitas
            ]
        )
        
        # Criação de um contexto com User-Agent para evitar detecção de bot
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        return pw, browser, context
        
    except Exception as e:
        # Garante que o Playwright seja encerrado se houver erro no launch
        await pw.stop()
        print(f"ERRO ao iniciar o navegador: {e}")
        raise e