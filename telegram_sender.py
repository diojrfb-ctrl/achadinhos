import os
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession
from database import salvar_como_postado
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env ou do painel do Render
load_dotenv()

# Configurações obtidas das suas variáveis de ambiente
api_id_env = os.getenv("API_ID")
api_hash = os.getenv("API_HASH")
string_session = os.getenv("STRING_SESSION")
canal_id = os.getenv("MEU_CANAL", "@OfertasFlashBR")

# Validação de segurança para garantir que as chaves existem
if not api_id_env or not api_hash or not string_session:
    print("❌ ERRO: API_ID, API_HASH ou STRING_SESSION em falta!")
    # No Render, isto aparecerá nos logs para o ajudar a diagnosticar
    api_id = 0 
else:
    api_id = int(api_id_env)

# Inicializa o cliente usando a StringSession (não precisa de ficheiro .session)
client = TelegramClient(StringSession(string_session), api_id, api_hash)

async def enviar_ao_telegram(produto: dict):
    """
    Recebe um dicionário com os dados do produto e envia para o canal.
    """
    try:
        # Garante que o cliente está ligado
        if not client.is_connected():
            await client.connect()

        # Montagem da legenda da foto com formatação Markdown
        # Nota: Usamos aspas simples f-string para evitar conflito com as aspas do dicionário
        legenda = (
            f"🔥 **{produto['titulo']}**\n\n"
            f"💰 Por apenas: **{produto['preco']}**\n"
        )
        
        if produto.get('preco_antigo'):
            legenda += f"❌ De: ~~{produto['preco_antigo']}~~\n"
            
        if produto.get('desconto'):
            legenda += f"📉 Desconto: **{produto['desconto']}**\n"
            
        legenda += f"\n🛒 **Link de Compra:** {produto['link']}"

        # Envio da mensagem com imagem
        # O Telethon aceita o URL da imagem diretamente no parâmetro 'file'
        await client.send_message(
            canal_id, 
            legenda, 
            file=produto['imagem'], 
            parse_mode='md'
        )
        
        # Após o envio com sucesso, guarda no Redis para não repetir
        salvar_como_postado(produto['asin'])
        print(f"✅ Oferta {produto['asin']} enviada com sucesso para o canal!")
        
    except Exception as e:
        print(f"❌ Erro ao enviar para o Telegram: {e}")

# Caso queira testar este ficheiro isoladamente (opcional)
if __name__ == "__main__":
    test_prod = {
        "asin": "TESTE",
        "titulo": "Produto de Teste",
        "preco": "R$ 99,90",
        "link": "https://amazon.com.br",
        "imagem": "https://m.media-amazon.com/images/I/51pX876+v6L._AC_SY450_.jpg"
    }
    loop = asyncio.get_event_loop()
    loop.run_until_complete(enviar_ao_telegram(test_prod))