import os
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv

# Importações dos seus módulos
try:
    from amazon_miner import minerar_amazon 
    from telegram_sender import enviar_ao_telegram
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")

load_dotenv()

# --- CONFIGURAÇÃO FLASK (Para o Render não matar o processo) ---
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot Achadinhos está online!", 200

def run_flask():
    # O Render usa a variável de ambiente PORT
    port = int(os.environ.get("PORT", 10000))
    print(f"🌍 Servidor Health Check rodando na porta {port}")
    app.run(host='0.0.0.0', port=port)

# --- LÓGICA DO BOT ---
async def engine():
    print("💎 Iniciar mineração de ofertas...")
    
    # Substitua pelas suas URLs reais
    URLS_AMAZON = [
        "https://www.amazon.com.br/gp/goldbox"
    ]
    STORE_ID = os.getenv("AMAZON_STORE_ID", "padrão-20")

    while True:
        try:
            print("🔍 Verificando novas ofertas na Amazon...")
            ofertas = await minerar_amazon(URLS_AMAZON, STORE_ID)
            
            if ofertas and len(ofertas) > 0:
                print(f"🔥 {len(ofertas)} ofertas encontradas!")
                for oferta in ofertas:
                    await enviar_ao_telegram(oferta)
                    await asyncio.sleep(2)  # Delay pequeno para não dar spam
            else:
                print("ℹ️ Nenhuma oferta nova encontrada neste ciclo.")

            # Espera 20 minutos (1200 segundos) para a próxima verificação
            print("💤 Aguardando 20 minutos para o próximo ciclo...")
            await asyncio.sleep(1200) 
            
        except Exception as e:
            print(f"❌ Erro crítico no loop: {e}")
            await asyncio.sleep(60) # Espera 1 minuto antes de tentar de novo

if __name__ == "__main__":
    # 1. Inicia o Flask em background
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

    # 2. Inicia o Bot
    try:
        asyncio.run(engine())
    except (KeyboardInterrupt, SystemExit):
        print("Bot encerrado.")