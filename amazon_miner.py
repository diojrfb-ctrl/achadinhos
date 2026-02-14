import asyncio
import re
from html import unescape
from typing import List, Dict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from browser import configurar_navegador
from database import ja_foi_postado

def converter_preco(texto: str) -> float:
    try:
        # Remove símbolos e converte vírgula em ponto
        limpo = re.sub(r'[^\d,]', '', texto).replace(',', '.')
        return float(limpo)
    except:
        return 0.0

async def minerar_amazon(urls: List[str], store_id: str) -> List[Dict[str, str]]:
    print("💎 Minerando Amazon...")
    produtos = []
    driver = configurar_navegador()

    try:
        for url in urls:
            driver.get(url)
            # Espera até que os itens da grade de ofertas apareçam
            await asyncio.sleep(7) 
            
            itens = driver.find_elements(By.XPATH, "//div[@data-asin and not(@data-asin='')]")
            print(f"📦 Itens encontrados na página: {len(itens)}")

            for item in itens:
                try:
                    asin = item.get_attribute("data-asin")
                    if not asin or ja_foi_postado(asin): 
                        continue

                    # Busca de dados com seletores mais flexíveis
                    titulo = item.find_element(By.TAG_NAME, "h2").text
                    
                    try:
                        p_int = item.find_element(By.CLASS_NAME, "a-price-whole").text
                        p_frac = item.find_element(By.CLASS_NAME, "a-price-fraction").text
                        preco_str = f"R$ {p_int},{p_frac}"
                    except:
                        continue # Se não tem preço, pula o item

                    img_url = item.find_element(By.TAG_NAME, "img").get_attribute("src")

                    # Lógica de Desconto
                    preco_antigo = ""
                    porcentagem = ""
                    try:
                        p_antigo_raw = item.find_element(By.CLASS_NAME, "a-text-price").find_element(By.CLASS_NAME, "a-offscreen").get_attribute("innerHTML")
                        preco_antigo = unescape(p_antigo_raw).strip()
                        
                        val_atual = converter_preco(preco_str)
                        val_antigo = converter_preco(preco_antigo)
                        
                        if val_antigo > val_atual and val_atual > 0:
                            desc = int((1 - (val_atual / val_antigo)) * 100)
                            porcentagem = f"{desc}% OFF"
                    except:
                        pass

                    produtos.append({
                        "asin": asin, 
                        "titulo": titulo, 
                        "imagem": img_url,
                        "link": f"https://www.amazon.com.br/dp/{asin}?tag={store_id}",
                        "preco": preco_str, 
                        "preco_antigo": preco_antigo,
                        "desconto": porcentagem
                    })
                    
                    if len(produtos) >= 10: 
                        break
                except Exception as e:
                    continue
    finally:
        driver.quit()
    
    return produtos