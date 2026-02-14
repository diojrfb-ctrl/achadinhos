import os
import asyncio
import threading
import signal
import sys
from flask import Flask
from dotenv import load_dotenv
from amazon_miner import AmazonMiner
from telegram_sender import TelegramSender
from config import AMAZON_STORE_ID, MEU_CANAL

load_dotenv()
app = Flask(__name__)

class OfertasFlashBot:
    """Bot principal de ofertas"""
    
    def __init__(self):
        self.store_id = os.getenv("AMAZON_STORE_ID", AMAZON_STORE_ID)
        self.canal = os.getenv("MEU_CANAL", MEU_CANAL)
        self.telegram = TelegramSender()
        self.miner = AmazonMiner(self.store_id)
        self.running = True
        self.urls_amazon = ["https://www.amazon.com.br/gp/goldbox"]
        
    def setup_signal_handlers(self):
        """Configura handlers para desligamento gracioso"""
        def signal_handler(sig, frame):
            print("\n🛑 Recebido sinal de desligamento...")
            self.running = False
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    async def iniciar(self):
        """Inicia o bot"""
        self.setup_signal_handlers()
        
        # Aguarda o servidor Flask iniciar
        await asyncio.sleep(5)
        
        await self.telegram.enviar_debug("🚀 Bot OfertasFlash inicializado no Render!")
        print("✅ Bot iniciado. Pressione Ctrl+C para parar.")
        
        while self.running:
            try:
                await self._executar_ciclo()
            except Exception as e:
                await self.telegram.enviar_debug(f"⚠️ Erro no ciclo: {str(e)[:100]}")
                await asyncio.sleep(60)
    
    async def _executar_ciclo(self):
        """Executa um ciclo completo de mineração e envio"""
        print(f"\n🔄 Iniciando ciclo em {asyncio.get_event_loop().time()}")
        
        # Mina as ofertas
        produtos = await self.miner.minerar(self.urls_amazon)
        
        # Envia as ofertas
        if produtos:
            print(f"📤 Enviando {len(produtos)} produtos...")
            for produto in produtos:
                await self.telegram.enviar_produto(produto.to_dict())
                await asyncio.sleep(5)  # Pausa entre envios
        
        # Aguarda próximo ciclo (20 minutos)
        print("💤 Aguardando 20 minutos até o próximo ciclo...")
        for _ in range(20):
            if not self.running:
                break
            await asyncio.sleep(60)  # 1 minuto
            
        await self.telegram.enviar_debug("💤 Ciclo finalizado. Aguardando próximo...")

# Rotas Flask
@app.route('/')
def health_check():
    return "🤖 OfertasFlashBR Bot Online!", 200

@app.route('/status')
def status():
    return {"status": "running", "timestamp": asyncio.get_event_loop().time()}, 200

def run_flask():
    """Roda o servidor Flask em uma thread separada"""
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Inicia Flask em thread separada
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Inicia o bot
    bot = OfertasFlashBot()
    
    try:
        asyncio.run(bot.iniciar())
    except KeyboardInterrupt:
        print("\n👋 Bot encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro fatal: {e}")
        sys.exit(1)