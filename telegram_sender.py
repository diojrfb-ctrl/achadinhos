import os
import asyncio
from telethon import TelegramClient
from database import salvar_como_postado
from dotenv import load_dotenv

load_dotenv()

# Configurações do Telegram obtidas via variáveis de ambiente
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
canal_id = os.getenv("TELEGRAM_CHAT_ID")

# Inicializa o cliente do Telegram
client = TelegramClient('bot_session', api_id, api_hash)

async def enviar_ao_telegram(produto: dict):
    """Formata e envia a oferta para o canal e marca como postado."""
    if not client.is_connected():
        await client.start(bot_token=bot_token)

    try:
        # Formatação da mensagem em Markdown
        mensagem = (
            f"🔥 **{produto['titulo']}**\n\n"
            f"💰 Por apenas: **{produto['preco']}**\n"
            f"{f'❌ De: ~~{produto['preco_antigo']}~~' if produto['preco_antigo'] else ''}\n"
            f"📉 Desconto: **{produto['desconto']}**\n\n"
            f"🛒 **Link de Compra:** {produto['link']}"
        )

        # Envio da imagem com a legenda formatada
        await client.send_message(canal_id, mensagem, file=produto['imagem'], parse_mode='md')
        
        # Salva no Redis para evitar duplicidade
        salvar_como_postado(produto['asin'])
        print(f"✅ Oferta {produto['asin']} enviada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro ao enviar para o Telegram: {e}")