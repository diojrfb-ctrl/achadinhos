import os
import subprocess
import sys

def check_playwright():
    print("🔍 Verificando instalação do Playwright...")
    
    # Verifica onde o Playwright está instalado
    result = subprocess.run([sys.executable, "-m", "playwright", "install", "--help"], 
                          capture_output=True, text=True)
    print(f"Playwright command: {result.returncode}")
    
    # Verifica o cache directory
    cache_dir = os.environ.get('PLAYWRIGHT_BROWSERS_PATH', 'Não definido')
    print(f"PLAYWRIGHT_BROWSERS_PATH: {cache_dir}")
    
    # Lista arquivos no cache
    possible_cache = "/opt/render/.cache/ms-playwright"
    if os.path.exists(possible_cache):
        print(f"✅ Cache existe em: {possible_cache}")
        print("Conteúdo:")
        os.system(f"ls -la {possible_cache}")
    else:
        print(f"❌ Cache não encontrado em: {possible_cache}")
    
    # Verifica home directory
    home_cache = os.path.expanduser("~/.cache/ms-playwright")
    if os.path.exists(home_cache):
        print(f"✅ Cache existe em: {home_cache}")
        print("Conteúdo:")
        os.system(f"ls -la {home_cache}")

if __name__ == "__main__":
    check_playwright()