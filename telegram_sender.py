import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from database import salvar_como_postado
from dotenv import load_dotenv

load_dotenv()

api_id_env = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
canal_principal = os.getenv("MEU_CANAL", "@OfertasFlashBR")
canal_debug = "@meusachadinhoslog" # Seu novo canal de debug

if not api_id_env or not api_hash or not string_session:
    print("❌ ERRO: Variáveis de ambiente do Telegram incompletas!")
    api_id = 0
else:
    api_id = int(api_id_env)

client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def enviar_debug(mensagem: str):
    """Envia logs de status e erros para o canal de debug."""
    try:
        if not client.is_connected():
            await client.connect()
        await client.send_message(canal_debug, f"🛠 **DEBUG LOG:**\n{mensagem}")
    except Exception as e:
        print(f"Falha ao enviar log para Telegram: {e}")

async def enviar_ao_telegram(produto: dict):
    """Envia a oferta formatada para o canal principal."""
    try:
        if not client.is_connected():
            await client.connect()

        legenda = (
            f"🔥 **{produto['titulo']}**\n\n"
            f"💰 Por apenas: **{produto['preco']}**\n"
        )
        if produto.get('preco_antigo'):
            legenda += f"❌ De: ~~{produto['preco_antigo']}~~\n"
        if produto.get('desconto'):
            legenda += f"📉 Desconto: **{produto['desconto']}**\n"
            
        legenda += f"\n🛒 **Link de Compra:** {produto['link']}"

        await client.send_message(canal_principal, legenda, file=produto['imagem'], parse_mode='md')
        
        salvar_como_postado(produto['asin'])
        await enviar_debug(f"✅ Sucesso: ASIN {produto['asin']} postado no canal principal.")
        
    except Exception as e:
        await enviar_debug(f"❌ ERRO ao enviar produto ao Telegram: {e}")