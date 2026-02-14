import os
import asyncio
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright otimizado para o ambiente Render.
    Versão compatível com Playwright 1.58.0
    """
    print("🔄 Iniciando Playwright...")
    pw = await async_playwright().start()
    
    try:
        # Playwright 1.58.0 usa chromium-1124
        cache_dir = os.path.expanduser("~/.cache/ms-playwright")
        render_cache = "/opt/render/.cache/ms-playwright"
        
        # Lista de possíveis caminhos para o executável
        caminhos_possiveis = [
            # Render.com cache
            "/opt/render/.cache/ms-playwright/chromium-1124/chrome-linux/chrome",
            "/opt/render/.cache/ms-playwright/chromium_headless_shell-1124/chrome-linux/chrome",
            # Home directory cache
            os.path.expanduser("~/.cache/ms-playwright/chromium-1124/chrome-linux/chrome"),
            os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1124/chrome-linux/chrome"),
            # Tentativa com versão mais recente
            "/opt/render/.cache/ms-playwright/chromium-1125/chrome-linux/chrome",
            os.path.expanduser("~/.cache/ms-playwright/chromium-1125/chrome-linux/chrome"),
        ]
        
        browser = None
        ultimo_erro = None
        
        # Primeiro, vamos verificar se os diretórios existem
        print("📁 Verificando diretórios de cache...")
        for diretorio in [cache_dir, render_cache]:
            if os.path.exists(diretorio):
                print(f"✅ Diretório encontrado: {diretorio}")
                try:
                    conteudo = os.listdir(diretorio)
                    print(f"   Conteúdo: {conteudo}")
                except:
                    print(f"   Não foi possível listar conteúdo")
            else:
                print(f"❌ Diretório não encontrado: {diretorio}")
        
        # Tenta cada caminho possível
        for caminho in caminhos_possiveis:
            try:
                if os.path.exists(caminho):
                    print(f"✅ Executável encontrado em: {caminho}")
                    print(f"🔄 Tentando iniciar browser com este executável...")
                    
                    browser = await pw.chromium.launch(
                        executable_path=caminho,
                        headless=True,
                        args=[
                            "--no-sandbox",
                            "--disable-dev-shm-usage",
                            "--disable-gpu",
                            "--disable-setuid-sandbox",
                            "--no-zygote",
                            "--disable-blink-features=AutomationControlled",
                        ]
                    )
                    print(f"✅ Browser iniciado com sucesso usando: {caminho}")
                    break
                else:
                    print(f"❌ Executável não encontrado: {caminho}")
            except Exception as e:
                ultimo_erro = e
                print(f"❌ Erro ao tentar {caminho}: {str(e)}")
                continue
        
        # Se não encontrou nenhum caminho, tenta sem especificar o executable_path
        if not browser:
            print("🔄 Nenhum executável encontrado. Tentando modo automático...")
            try:
                browser = await pw.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-dev-shm-usage",
                        "--disable-gpu",
                        "--disable-setuid-sandbox",
                        "--no-zygote",
                    ]
                )
                print("✅ Browser iniciado em modo automático!")
            except Exception as e:
                ultimo_erro = e
                print(f"❌ Erro no modo automático: {e}")
        
        if not browser:
            erro_msg = f"Não foi possível iniciar o browser. Último erro: {ultimo_erro}"
            print(f"❌ {erro_msg}")
            raise Exception(erro_msg)
        
        # Cria o contexto
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 720}
        )
        
        print("✅ Contexto do browser criado com sucesso!")
        return pw, browser, context
        
    except Exception as e:
        print(f"❌ Erro fatal em obter_browser: {e}")
        if pw:
            await pw.stop()
        raise e