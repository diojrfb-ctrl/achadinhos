import asyncio
import re
from html import unescape
from typing import List, Dict
from selenium.webdriver.common.by import By
from browser import configurar_navegador
from database import ja_foi_postado

def converter_preco(texto: str) -> float:
    try:
        return float(re.sub(r'[^\d,]', '', texto).replace(',', '.'))
    except:
        return 0.0

async def minerar_amazon(urls: List[str], store_id: str) -> List[Dict[str, str]]:
    print("💎 Minerando Amazon...")
    produtos = []
    driver = configurar_navegador()

    try:
        for url in urls:
            driver.get(url)
            await asyncio.sleep(8) # Tempo maior para carregar no Render
            
            # Busca itens com ASIN (produtos reais)
            itens = driver.find_elements(By.XPATH, "//div[@data-asin and not(@data-asin='')]")

            for item in itens:
                try:
                    asin = item.get_attribute("data-asin")
                    if not asin or ja_foi_postado(asin): continue

                    titulo = item.find_element(By.TAG_NAME, "h2").text
                    
                    # Tentativa robusta de pegar o preço
                    try:
                        p_int = item.find_element(By.CLASS_NAME, "a-price-whole").text
                        p_frac = item.find_element(By.CLASS_NAME, "a-price-fraction").text
                        preco_str = f"R$ {p_int},{p_frac}"
                    except:
                        # Fallback caso o seletor mude
                        preco_str = item.find_element(By.CLASS_NAME, "a-offscreen").get_attribute("innerText")
                    
                    img_url = item.find_element(By.TAG_NAME, "img").get_attribute("src")

                    # Cálculo de Desconto
                    preco_antigo = ""
                    porcentagem = ""
                    try:
                        p_antigo_raw = item.find_element(By.CLASS_NAME, "a-text-price").find_element(By.CLASS_NAME, "a-offscreen").get_attribute("innerHTML")
                        preco_antigo = unescape(p_antigo_raw).strip()
                        
                        v_atual = converter_preco(preco_str)
                        v_antigo = converter_preco(preco_antigo)
                        
                        if v_antigo > v_atual:
                            porcentagem = f"{int((1 - (v_atual / v_antigo)) * 100)}% OFF"
                    except: pass

                    produtos.append({
                        "asin": asin, "titulo": titulo, "imagem": img_url,
                        "link": f"https://www.amazon.com.br/dp/{asin}?tag={store_id}",
                        "preco": preco_str, "preco_antigo": preco_antigo,
                        "desconto": porcentagem
                    })
                    if len(produtos) >= 10: break
                except: continue
    finally:
        driver.quit()
    return produtos