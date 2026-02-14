import re

def convert_to_amazon_affiliate(url: str, store_id: str) -> str:
    """
    Transforma um link comum da Amazon em um link com seu ID de associado.
    """
    if "amazon.com.br" in url:
        # Remove parâmetros antigos de rastreio se existirem
        base_url = url.split('?')[0]
        # Adiciona o seu StoreID
        affiliate_url = f"{base_url}?tag={store_id}"
        return affiliate_url
    return url



