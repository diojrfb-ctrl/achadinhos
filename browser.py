import os
import asyncio
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright otimizado para o ambiente Render.
    """
    pw = await async_playwright().start()
    
    try:
        # Tenta diferentes caminhos baseados na versão 1.58.0
        caminhos_possiveis = [
            "/opt/render/.cache/ms-playwright/chromium-1124/chrome-linux/chrome",
            "/opt/render/.cache/ms-playwright/chromium_headless_shell-1124/chrome-linux/chrome",
            os.path.expanduser("~/.cache/ms-playwright/chromium-1124/chrome-linux/chrome"),
            os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1124/chrome-linux/chrome"),
            None  # Auto-detect
        ]
        
        browser = None
        ultimo_erro = None
        
        for caminho in caminhos_possiveis:
            try:
                launch_args = {
                    "headless": True,
                    "args": [
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--disable-setuid-sandbox",
                        "--no-zygote",
                        "--single-process",
                        "--disable-blink-features=AutomationControlled"
                    ]
                }
                
                if caminho:
                    launch_args["executable_path"] = caminho
                    print(f"🔄 Tentando executável: {caminho}")
                else:
                    print("🔄 Tentando modo automático")
                
                browser = await pw.chromium.launch(**launch_args)
                print(f"✅ Browser iniciado com sucesso!")
                break
                
            except Exception as e:
                ultimo_erro = e
                print(f"❌ Falha: {str(e)[:100]}")
                continue
        
        if not browser:
            print("❌ Todas as tentativas falharam!")
            print(f"❌ Último erro: {ultimo_erro}")
            raise Exception("Não foi possível iniciar o browser")
        
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        print("✅ Contexto do browser criado")
        return pw, browser, context
        
    except Exception as e:
        if pw:
            await pw.stop()
        print(f"❌ Erro fatal: {e}")
        raise e