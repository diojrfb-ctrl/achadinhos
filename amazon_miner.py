import asyncio
from typing import List, Dict
from browser import obter_browser
from database import ja_foi_postado
from telegram_sender import enviar_debug

async def minerar_amazon(urls: List[str], store_id: str) -> List[Dict[str, str]]:
    await enviar_debug("🔍 Iniciando mineração com motor Playwright...")
    produtos = []
    
    try:
        pw, browser, context = await obter_browser()
        page = await context.new_page()

        for url in urls:
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await page.evaluate("window.scrollBy(0, 800)") # Scroll para carregar imagens
            await asyncio.sleep(5)
            
            # Localiza os blocos de produtos
            itens = await page.query_selector_all("div[data-asin]:not([data-asin=''])")
            await enviar_debug(f"Página carregada. Blocos de produtos (ASIN) encontrados: {len(itens)}")

            for item in itens:
                try:
                    asin = await item.get_attribute("data-asin")
                    if not asin or ja_foi_postado(asin):
                        continue

                    # Captura Título
                    titulo_el = await item.query_selector("h2")
                    titulo = await titulo_el.inner_text() if titulo_el else "Produto sem título"

                    # Captura Preço
                    preco = "Ver na loja"
                    p_el = await item.query_selector(".a-price-whole")
                    if p_el:
                        p_frac = await item.query_selector(".a-price-fraction")
                        frac_text = await p_frac.inner_text() if p_frac else "00"
                        preco = f"R$ {await p_el.inner_text()},{frac_text}".replace("\n", "")
                    else:
                        p_off = await item.query_selector(".a-offscreen")
                        if p_off: preco = await p_off.inner_text()

                    # Captura Imagem
                    img_el = await item.query_selector("img")
                    img_url = await img_el.get_attribute("src") if img_el else ""

                    produtos.append({
                        "asin": asin,
                        "titulo": titulo.strip()[:100] + "...",
                        "imagem": img_url,
                        "link": f"https://www.amazon.com.br/dp/{asin}?tag={store_id}",
                        "preco": preco,
                    })

                    if len(produtos) >= 5: break
                except:
                    continue
                    
        await browser.close()
        await pw.stop()
        
    except Exception as e:
        await enviar_debug(f"🚨 Erro na extração Playwright: {str(e)[:150]}")
    
    return produtos