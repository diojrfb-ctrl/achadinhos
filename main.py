import os
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from amazon_miner import minerar_amazon 
from telegram_sender import enviar_ao_telegram, enviar_debug
from config import AMAZON_STORE_ID

load_dotenv()
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot Online", 200

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def engine():
    await asyncio.sleep(5) # Aguarda o servidor Flask subir
    await enviar_debug("🚀 Motor do Bot inicializado com sucesso no Render!")
    
    urls_amazon = ["https://www.amazon.com.br/gp/goldbox"]
    store_id = os.getenv("AMAZON_STORE_ID", AMAZON_STORE_ID)

    while True:
        try:
            ofertas = await minerar_amazon(urls_amazon, store_id)
            
            if ofertas:
                for oferta in ofertas:
                    await enviar_ao_telegram(oferta)
                    await asyncio.sleep(5) 
            
            # Log de espera para você saber que o bot não travou
            await asyncio.sleep(1200) # 20 minutos
            await enviar_debug("💤 Ciclo finalizado. Aguardando próximo intervalo...")
            
        except Exception as e:
            await enviar_debug(f"⚠️ Erro no loop principal (Engine): {e}")
            await asyncio.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.run(engine())