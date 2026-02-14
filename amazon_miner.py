import asyncio
from typing import List, Dict
from browser import obter_browser
from database import ja_foi_postado
from telegram_sender import enviar_debug

async def minerar_amazon(urls: List[str], store_id: str) -> List[Dict[str, str]]:
    await enviar_debug("🌐 Abrindo navegador para mineração...")
    produtos = []
    
    try:
        pw, browser, context = await obter_browser()
        page = await context.new_page()

        for url in urls:
            await enviar_debug(f"🔍 Acessando Amazon: {url}")
            # Timeout longo para evitar erros em instâncias gratuitas
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            
            # Pequena rolagem para ativar carregamento de imagens
            await page.mouse.wheel(0, 1500)
            await asyncio.sleep(5)
            
            itens = await page.query_selector_all("div[data-asin]:not([data-asin=''])")
            await enviar_debug(f"📦 Blocos detectados: {len(itens)}")

            for item in itens:
                try:
                    asin = await item.get_attribute("data-asin")
                    if not asin or ja_foi_postado(asin): continue

                    titulo_el = await item.query_selector("h2")
                    titulo = await titulo_el.inner_text() if titulo_el else "Produto Amazon"

                    preco = "Ver Preço"
                    p_el = await item.query_selector(".a-price-whole")
                    if p_el:
                        preco = f"R$ {await p_el.inner_text()}".replace("\n", "")

                    img_el = await item.query_selector("img")
                    img_url = await img_el.get_attribute("src") if img_el else ""

                    produtos.append({
                        "asin": asin,
                        "titulo": titulo.strip()[:80],
                        "imagem": img_url,
                        "link": f"https://www.amazon.com.br/dp/{asin}?tag={store_id}",
                        "preco": preco,
                    })

                    if len(produtos) >= 5: break
                except: continue
                    
        await browser.close()
        await pw.stop()
        
    except Exception as e:
        await enviar_debug(f"🚨 Erro no Minerador: {str(e)[:150]}")
    
    return produtos