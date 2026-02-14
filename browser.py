import os
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright garantindo que o executável seja encontrado 
    no ambiente do Render.
    """
    # Força o Playwright a olhar para o diretório de cache padrão do Render
    # ou para onde o comando de build instalou os binários.
    pw = await async_playwright().start()
    
    try:
        # Lançamos o navegador sem definir executable_path manualmente.
        # Ao usar chromium_headless_shell, economizamos RAM.
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--single-process"
            ]
        )
        
        # Contexto com User-Agent para evitar bloqueios
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        return pw, browser, context
        
    except Exception as e:
        # Fecha o motor em caso de erro para evitar processos zumbis
        await pw.stop()
        print(f"ERRO CRÍTICO no navegador: {e}")
        raise e