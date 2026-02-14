import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from database import salvar_como_postado
from dotenv import load_dotenv

load_dotenv()

api_id = int(os.getenv("API_ID", 0))
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
canal_principal = os.getenv("MEU_CANAL", "@OfertasFlashBR")
canal_debug = "@meusachadinhoslog" 

client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def enviar_debug(mensagem: str):
    try:
        if not client.is_connected():
            await client.connect()
        await client.send_message(canal_debug, f"🛠 **LOG:** {mensagem}")
    except Exception as e:
        print(f"Erro log: {e}")

async def enviar_ao_telegram(produto: dict):
    try:
        if not client.is_connected():
            await client.connect()

        legenda = (
            f"🔥 **{produto['titulo']}**\n\n"
            f"💰 Por apenas: **{produto['preco']}**\n"
            f"\n🛒 **Link de Compra:** {produto['link']}"
        )

        await client.send_message(canal_principal, legenda, file=produto['imagem'], parse_mode='md')
        salvar_como_postado(produto['asin'])
    except Exception as e:
        await enviar_debug(f"ERRO Envio: {e}")