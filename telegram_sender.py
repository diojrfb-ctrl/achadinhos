import os
from telethon import TelegramClient
from telethon.sessions import StringSession
from database import salvar_como_postado
from dotenv import load_dotenv

load_dotenv()

class TelegramSender:
    """Gerenciador de envios para o Telegram"""
    
    def __init__(self):
        self.api_id = int(os.getenv("API_ID", 0))
        self.api_hash = os.getenv("API_HASH")
        self.string_session = os.getenv("STRING_SESSION")
        self.canal_principal = os.getenv("MEU_CANAL", "@OfertasFlashBR")
        self.canal_debug = "@meusachadinhoslog"
        self.client = None
        self._conectado = False
    
    async def _conectar(self):
        """Conecta ao Telegram se necessário"""
        if not self._conectado:
            self.client = TelegramClient(
                StringSession(self.string_session), 
                self.api_id, 
                self.api_hash
            )
            await self.client.connect()
            self._conectado = True
    
    async def enviar_debug(self, mensagem: str):
        """Envia mensagem de debug"""
        try:
            await self._conectar()
            await self.client.send_message(
                self.canal_debug, 
                f"🛠 **LOG:** {mensagem}",
                parse_mode='md'
            )
        except Exception as e:
            print(f"Erro ao enviar debug: {e}")
    
    async def enviar_produto(self, produto: dict):
        """Envia um produto para o canal principal"""
        try:
            await self._conectar()
            
            # Formata a mensagem
            legenda = self._formatar_mensagem(produto)
            
            # Envia com imagem se disponível
            if produto.get('imagem'):
                await self.client.send_message(
                    self.canal_principal,
                    legenda,
                    file=produto['imagem'],
                    parse_mode='md'
                )
            else:
                await self.client.send_message(
                    self.canal_principal,
                    legenda,
                    parse_mode='md'
                )
            
            # Marca como postado
            salvar_como_postado(produto['asin'])
            print(f"✅ Produto enviado: {produto['titulo'][:50]}...")
            
        except Exception as e:
            await self.enviar_debug(f"❌ Erro no envio: {str(e)[:100]}")
            print(f"Erro no envio: {e}")
    
    def _formatar_mensagem(self, produto: dict) -> str:
        """Formata a mensagem do produto"""
        return (
            f"🔥 **{produto['titulo']}**\n\n"
            f"💰 Por apenas: **{produto['preco']}**\n"
            f"\n🛒 **Compre aqui:** {produto['link']}\n\n"
            f"#{produto['asin']}"
        )

# Funções de compatibilidade
async def enviar_debug(mensagem: str):
    sender = TelegramSender()
    await sender.enviar_debug(mensagem)

async def enviar_ao_telegram(produto: dict):
    sender = TelegramSender()
    await sender.enviar_produto(produto)