import os
from upstash_redis import Redis
from dotenv import load_dotenv

load_dotenv()

# Configurações do Upstash Redis
redis = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)

def ja_foi_postado(asin: str) -> bool:
    # Verifica se a chave existe no Redis
    return redis.exists(f"postado:{asin}") == 1

def salvar_como_postado(asin: str):
    # Salva com expiração de 7 dias (604800 segundos)
    # pois o produto pode entrar em promoção novamente depois de uma semana
    redis.set(f"postado:{asin}", "true", ex=604800)