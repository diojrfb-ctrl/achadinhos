import os
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright e o navegador Chromium de forma dinâmica.
    Removemos a busca manual por caminhos (glob) para evitar erros de versão.
    """
    # Inicializa o motor do Playwright
    pw = await async_playwright().start()
    
    try:
        # Lançamos o browser sem definir 'executable_path' manualmente.
        # O Playwright encontrará o binário correto automaticamente se ele 
        # for instalado via comando de build no Render.
        browser = await pw.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox", 
                "--disable-dev-shm-usage",
                "--disable-setuid-sandbox",
                "--no-zygote",
                "--single-process" # Recomendado para instâncias com pouca RAM (Free Tier)
            ]
        )
        
        # Cria um novo contexto com um User-Agent real para evitar bloqueios da Amazon
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        return pw, browser, context
        
    except Exception as e:
        # Se falhar ao abrir o navegador, encerramos o Playwright para evitar vazamento de memória
        await pw.stop()
        print(f"ERRO CRÍTICO ao iniciar o navegador: {e}")
        raise e