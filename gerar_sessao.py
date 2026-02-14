import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

# Seus dados
API_ID: int = 32407152
API_HASH: str = "db653015ecc7401831ad83298cb6605d"


async def main() -> None:
    # Criamos o cliente com uma sessão vazia
    client = TelegramClient(StringSession(), API_ID, API_HASH)

    print("🚀 Iniciando processo de login...")
    await client.connect()

    # Se não estiver logado, inicia o fluxo manual
    if not await client.is_user_authorized():
        # 1. Pede o telefone
        phone: str = input("📞 Digite seu telefone (ex: +5511999999999): ")
        await client.send_code_request(phone)

        # 2. Pede o código do Telegram
        code: str = input("🔢 Digite o código que recebeu no Telegram: ")

        try:
            # Tenta logar apenas com o código
            await client.sign_in(phone, code)
        except Exception:
            # 3. Se falhar (provavelmente pelo 2FA), ele pede a senha aqui
            print("🔐 2FA Detectado! Por favor, insira sua senha.")
            password: str = input("🔑 Digite sua senha de Verificação em Duas Etapas: ")
            await client.sign_in(password=password)

    # Se chegou aqui, logou!
    session_string: str = client.session.save()

    print("\n" + "=" * 60)
    print("✅ SUCESSO! COPIE A STRING ABAIXO:")
    print("=" * 60 + "\n")
    print(session_string)
    print("\n" + "=" * 60)
    print("⚠️  Agora cole esse código no seu .env em STRING_SESSION.")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())