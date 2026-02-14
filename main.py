import os
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv

try:
    from amazon_miner import minerar_amazon 
    from telegram_sender import enviar_ao_telegram
    from config import AMAZON_STORE_ID
except ImportError as e:
    print(f"❌ Erro crítico de importação: {e}")

load_dotenv()
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot Achadinhos está online!", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    print(f"🌍 Servidor Health Check ativo na porta {port}")
    app.run(host='0.0.0.0', port=port)

async def engine():
    print("💎 Iniciando motor de busca...")
    urls_amazon = ["https://www.amazon.com.br/gp/goldbox"]
    store_id = os.getenv("AMAZON_STORE_ID", AMAZON_STORE_ID)

    while True:
        try:
            print("🔍 Buscando novas ofertas...")
            ofertas = await minerar_amazon(urls_amazon, store_id)
            
            if ofertas:
                print(f"🔥 {len(ofertas)} novas ofertas encontradas.")
                for oferta in ofertas:
                    await enviar_ao_telegram(oferta)
                    await asyncio.sleep(5) 
            else:
                print("ℹ️ Nenhuma oferta nova encontrada.")

            print("💤 Aguardando 20 minutos...")
            await asyncio.sleep(1200)
            
        except Exception as e:
            print(f"❌ Erro no engine: {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    try:
        asyncio.run(engine())
    except (KeyboardInterrupt, SystemExit):
        print("Bot finalizado.")