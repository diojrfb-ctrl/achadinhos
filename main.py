import os
import asyncio
import requests
import io
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.sessions import StringSession

# Importando nossos componentes
from amazon_miner import minerar_amazon
from database import salvar_como_postado

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
STRING_SESSION = os.getenv("STRING_SESSION")
MEU_CANAL = os.getenv("MEU_CANAL")
STORE_ID = os.getenv("StoreID")

URLS_AMAZON = [
    "https://www.amazon.com.br/s?k=eletronicos&rh=p_85%3A19173332011%2Cp_n_pct-off-with-tax%3A10-",
    "https://www.amazon.com.br/s?k=cozinha&rh=p_85%3A19173332011%2Cp_n_pct-off-with-tax%3A15-"
]

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)


async def postar_oferta(p):
    header = f"🔥 {p['desconto']} de ECONOMIA!" if p['desconto'] else "💎 OPORTUNIDADE ÚNICA!"
    texto = (
        f"{header}\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"📦 **{p['titulo']}**\n\n"
        f"💰 **VALORES:**\n"
        f"❌ De: ~~{p['preco_antigo'] if p['preco_antigo'] else 'Preço Normal'}~~\n"
        f"✅ **Por: {p['preco']}**\n\n"
        f"🛒 **LINK OFICIAL:**\n{p['link']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )

    res = requests.get(p['imagem'], timeout=10)
    foto = io.BytesIO(res.content)
    foto.name = "oferta.jpg"
    await client.send_message(MEU_CANAL, texto, file=foto, parse_mode='markdown')
    salvar_como_postado(p['asin'])


async def engine():
    await client.start()
    while True:
        # Futuramente você fará: ofertas = await minerar_amazon(...) + await minerar_shopee(...)
        ofertas = await minerar_amazon(URLS_AMAZON, STORE_ID)

        for p in ofertas:
            try:
                await postar_oferta(p)
                await asyncio.sleep(180)  # Delay entre posts
            except Exception as e:
                print(f"Erro: {e}")

        print("Ciclo finalizado. Aguardando próximo agendamento.")
        await asyncio.sleep(2700)


if __name__ == "__main__":
    asyncio.run(engine())