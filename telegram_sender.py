import os
import asyncio
from telethon import TelegramClient
from database import salvar_como_postado
from dotenv import load_dotenv

load_dotenv()

# --- CORREÇÃO AQUI ---
# Usamos int() para o API_ID e garantimos que os nomes batam com o seu log
api_id_env = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
bot_token = os.getenv("BOT_TOKEN") # Ou TELEGRAM_BOT_TOKEN conforme seu .env
canal_id = os.getenv("MEU_CANAL")   # Usando o nome que você postou: MEU_CANAL

if not api_id_env or not api_hash:
    raise ValueError("ERRO: API_ID ou API_HASH não encontrados nas variáveis de ambiente do Render!")

api_id = int(api_id_env)
api_hash = str(api_hash)

# Inicializa o cliente
client = TelegramClient('bot_session', api_id, api_hash)

async def enviar_ao_telegram(produto: dict):
    """Formata e envia a oferta para o canal."""
    try:
        if not client.is_connected():
            await client.start(bot_token=bot_token)

        # Formatação da mensagem
        mensagem = (
            f"🔥 **{produto['titulo']}**\n\n"
            f"💰 Por apenas: **{produto['preco']}**\n"
            f"{f'❌ De: ~~{produto['preco_antigo']}~~' if produto['preco_antigo'] else ''}\n"
            f"📉 Desconto: **{produto['desconto']}**\n\n"
            f"🛒 **Link de Compra:** {produto['link']}"
        )

        # Envio
        await client.send_message(canal_id, mensagem, file=produto['imagem'], parse_mode='md')
        
        # Salva no Redis para evitar duplicidade
        salvar_como_postado(produto['asin'])
        print(f"✅ Oferta {produto['asin']} enviada para {canal_id}")
        
    except Exception as e:
        print(f"❌ Erro ao enviar para o Telegram: {e}")