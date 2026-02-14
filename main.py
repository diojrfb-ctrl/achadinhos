import os
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv

# Importe suas funções de mineração aqui
# Certifique-se de que os nomes dos arquivos/funções batem com os seus
from amazon_miner import minerar_amazon 
from telegram_sender import enviar_ao_telegram

# Carrega as variáveis do arquivo .env (local) ou do Render (produção)
load_dotenv()

# Configurações do Flask para o Render não derrubar o serviço
app = Flask(__name__)

@app.route('/')
def health_check():
    return "Bot Achadinhos está online!", 200

def run_flask():
    # O Render exige que o app escute na porta definida pela variável PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

async def engine():
    """Função principal que coordena a mineração e o envio"""
    print("💎 Minerando ofertas...")
    
    # Exemplo de URLs e ID da loja (ajuste conforme sua lógica)
    URLS_AMAZON = [
        "https://www.amazon.com.br/gp/goldbox",
        "https://www.amazon.com.br/b?node=16215417011"
    ]
    STORE_ID = os.getenv("AMAZON_STORE_ID", "seu_id-20")

    while True:
        try:
            # 1. Minera as ofertas
            ofertas = await minerar_amazon(URLS_AMAZON, STORE_ID)
            
            if ofertas:
                print(f"🔥 {len(ofertas)} novas ofertas encontradas!")
                # 2. Envia para o Telegram
                for oferta in ofertas:
                    await enviar_ao_telegram(oferta)
            else:
                print("Wait... Nenhuma oferta nova agora.")

            # 3. Espera X minutos antes de minerar de novo (ex: 15 min)
            print("💤 Aguardando próximo ciclo...")
            await asyncio.sleep(900) 
            
        except Exception as e:
            print(f"❌ Erro no loop principal: {e}")
            await asyncio.sleep(60) # Espera 1 minuto antes de tentar de novo após erro

if __name__ == "__main__":
    # 1. Inicia o servidor Flask em uma thread separada
    print("🌍 Iniciando servidor de monitoramento...")
    threading.Thread(target=run_flask, daemon=True).start()

    # 2. Inicia o loop assíncrono do Bot
    try:
        asyncio.run(engine())
    except KeyboardInterrupt:
        print("Bot desligado manualmente.")