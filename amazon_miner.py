import asyncio
from typing import List, Dict
from browser import obter_browser
from database import ja_foi_postado
from telegram_sender import enviar_debug

async def minerar_amazon(urls: List[str], store_id: str) -> List[Dict[str, str]]:
    await enviar_debug("🌐 Abrindo navegador para mineração...")
    print("🌐 Iniciando mineração...")  # Log local também
    produtos = []
    
    try:
        print("📦 Obtendo browser...")
        pw, browser, context = await obter_browser()
        page = await context.new_page()
        print("✅ Página criada")

        for url in urls:
            await enviar_debug(f"🔍 Acessando Amazon: {url}")
            print(f"🔍 Acessando: {url}")
            
            # Timeout longo para evitar erros
            await page.goto(url, wait_until="domcontentloaded", timeout=90000)
            print("✅ Página carregada")
            
            # Pequena rolagem para ativar carregamento
            await page.mouse.wheel(0, 1500)
            await asyncio.sleep(3)
            
            # Aguarda um pouco para garantir carregamento
            await page.wait_for_timeout(2000)
            
            # Tenta diferentes seletores
            itens = await page.query_selector_all("div[data-asin]:not([data-asin=''])")
            print(f"📦 Itens encontrados: {len(itens)}")
            await enviar_debug(f"📦 Blocos detectados: {len(itens)}")

            if len(itens) == 0:
                # Tenta seletor alternativo
                itens = await page.query_selector_all("[data-asin]")
                print(f"📦 Itens (seletor alternativo): {len(itens)}")

            for item in itens:
                try:
                    asin = await item.get_attribute("data-asin")
                    if not asin or len(asin.strip()) == 0 or ja_foi_postado(asin):
                        continue

                    print(f"✅ Novo ASIN encontrado: {asin}")

                    # Título
                    titulo = "Produto Amazon"
                    titulo_el = await item.query_selector("h2")
                    if titulo_el:
                        titulo = await titulo_el.inner_text()
                    else:
                        titulo_el = await item.query_selector(".a-size-base-plus")
                        if titulo_el:
                            titulo = await titulo_el.inner_text()

                    # Preço
                    preco = "Ver Preço"
                    p_el = await item.query_selector(".a-price-whole")
                    if p_el:
                        preco_texto = await p_el.inner_text()
                        preco = f"R$ {preco_texto}".replace("\n", "")
                    else:
                        p_el = await item.query_selector(".a-price")
                        if p_el:
                            preco = "Ver preço na Amazon"

                    # Imagem
                    img_url = ""
                    img_el = await item.query_selector("img")
                    if img_el:
                        img_url = await img_el.get_attribute("src")
                        # Pega imagem de maior qualidade
                        if img_url and "._" in img_url:
                            img_url = img_url.split("._")[0] + ".jpg"

                    produto = {
                        "asin": asin,
                        "titulo": titulo.strip()[:100],
                        "imagem": img_url,
                        "link": f"https://www.amazon.com.br/dp/{asin}?tag={store_id}",
                        "preco": preco,
                    }
                    
                    produtos.append(produto)
                    print(f"✅ Produto adicionado: {titulo[:50]}...")
                    
                    if len(produtos) >= 5:
                        break
                        
                except Exception as e:
                    print(f"⚠️ Erro processando item: {e}")
                    continue
                    
        print(f"📊 Total de produtos minerados: {len(produtos)}")
        await browser.close()
        await pw.stop()
        print("✅ Browser fechado")
        
    except Exception as e:
        erro_msg = f"🚨 Erro no Minerador: {str(e)[:200]}"
        print(erro_msg)
        await enviar_debug(erro_msg)
    
    return produtos