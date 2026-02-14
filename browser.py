import os
import asyncio
from playwright.async_api import async_playwright

async def obter_browser():
    """
    Inicializa o Playwright otimizado para o ambiente Render.
    Versão compatível com Playwright que procura chromium_headless_shell-1208
    """
    print("🔄 Iniciando Playwright...")
    pw = await async_playwright().start()
    
    try:
        # Caminhos específicos para a versão 1208 que o log mostra
        caminhos_possiveis = [
            # O caminho exato que o erro mostra
            "/opt/render/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell",
            "/opt/render/.cache/ms-playwright/chromium-1208/chrome-linux/chrome",
            "/opt/render/.cache/ms-playwright/chromium_headless_shell-1208/chrome-linux/chrome",
            # Cache no home directory
            os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell"),
            os.path.expanduser("~/.cache/ms-playwright/chromium-1208/chrome-linux/chrome"),
        ]
        
        browser = None
        ultimo_erro = None
        
        print("📁 Verificando caminhos para Chromium 1208...")
        
        # Primeiro, vamos verificar se o diretório base existe
        base_dir = "/opt/render/.cache/ms-playwright"
        if os.path.exists(base_dir):
            print(f"✅ Diretório base encontrado: {base_dir}")
            try:
                conteudo = os.listdir(base_dir)
                print(f"📂 Pastas disponíveis: {[d for d in conteudo if 'chromium' in d]}")
            except:
                print("❌ Erro ao listar conteúdo")
        
        # Tenta cada caminho possível
        for caminho in caminhos_possiveis:
            try:
                if os.path.exists(caminho):
                    print(f"✅ Executável encontrado: {caminho}")
                    print(f"🔄 Tentando iniciar browser...")
                    
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
                    print(f"✅ Browser iniciado com sucesso!")
                    break
                else:
                    print(f"❌ Executável não encontrado: {caminho}")
            except Exception as e:
                ultimo_erro = e
                print(f"❌ Erro ao tentar {caminho}: {str(e)[:100]}")
                continue
        
        # Se não encontrou, tenta encontrar automaticamente
        if not browser:
            print("🔄 Buscando automaticamente por executáveis do Chromium...")
            
            # Procura por qualquer executável chromium no cache
            find_cmd = "find /opt/render/.cache/ms-playwright -name chrome -o -name chrome-headless-shell -type f 2>/dev/null | head -3"
            import subprocess
            result = subprocess.run(find_cmd, shell=True, capture_output=True, text=True)
            
            if result.stdout:
                caminhos_encontrados = result.stdout.strip().split('\n')
                for caminho in caminhos_encontrados:
                    if caminho and os.path.exists(caminho):
                        print(f"🔄 Tentando executável encontrado: {caminho}")
                        try:
                            browser = await pw.chromium.launch(
                                executable_path=caminho,
                                headless=True,
                                args=["--no-sandbox", "--disable-dev-shm-usage"]
                            )
                            print(f"✅ Browser iniciado com: {caminho}")
                            break
                        except Exception as e:
                            print(f"❌ Falha com {caminho}: {e}")
                            continue
        
        # Última tentativa: modo automático
        if not browser:
            print("🔄 Última tentativa: modo automático")
            try:
                browser = await pw.chromium.launch(
                    headless=True,
                    args=["--no-sandbox", "--disable-dev-shm-usage"]
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