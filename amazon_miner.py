import asyncio
from typing import List, Dict, Optional
from dataclasses import dataclass
from browser import BrowserManager
from database import ja_foi_postado
from telegram_sender import enviar_debug

@dataclass
class ProdutoAmazon:
    """Modelo de dados para produtos da Amazon"""
    asin: str
    titulo: str
    preco: str
    link: str
    imagem: Optional[str] = None
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "asin": self.asin,
            "titulo": self.titulo,
            "preco": self.preco,
            "link": self.link,
            "imagem": self.imagem or ""
        }

class AmazonMiner:
    """Minerador de ofertas da Amazon"""
    
    def __init__(self, store_id: str, max_produtos: int = 5):
        self.store_id = store_id
        self.max_produtos = max_produtos
        self.selectors = {
            "produto": "div[data-asin]:not([data-asin=''])",
            "titulo": ["h2", ".a-size-base-plus", ".a-size-medium"],
            "preco": [".a-price-whole", ".a-price", ".a-offscreen"],
            "imagem": "img",
            "titulo_alternativo": "[data-cy='title-recipe']"
        }
    
    async def minerar(self, urls: List[str]) -> List[ProdutoAmazon]:
        """Minerar ofertas das URLs fornecidas"""
        
        await enviar_debug("🌐 Iniciando mineração...")
        produtos_encontrados = []
        
        async with BrowserManager() as browser_manager:
            page = await browser_manager.context.new_page()
            
            for url in urls:
                try:
                    produtos_url = await self._minerar_url(page, url)
                    produtos_encontrados.extend(produtos_url)
                    
                    if len(produtos_encontrados) >= self.max_produtos:
                        break
                        
                except Exception as e:
                    await enviar_debug(f"⚠️ Erro na URL {url}: {str(e)[:100]}")
                    continue
            
            await page.close()
        
        await enviar_debug(f"✅ Mineração concluída: {len(produtos_encontrados)} produtos")
        return produtos_encontrados[:self.max_produtos]
    
    async def _minerar_url(self, page, url: str) -> List[ProdutoAmazon]:
        """Minerar produtos de uma URL específica"""
        produtos = []
        
        print(f"🔍 Acessando: {url}")
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # Aguarda carregamento inicial
        await asyncio.sleep(2)
        
        # Rola a página para carregar mais produtos
        await self._scroll_page(page)
        
        # Encontra os elementos de produto
        elementos = await page.query_selector_all(self.selectors["produto"])
        print(f"📦 Elementos encontrados: {len(elementos)}")
        
        for elemento in elementos[:self.max_produtos * 2]:  # Pega mais para filtrar
            try:
                produto = await self._extrair_produto(elemento)
                if produto and not ja_foi_postado(produto.asin):
                    produtos.append(produto)
                    print(f"✅ Novo produto: {produto.titulo[:50]}...")
                    
                    if len(produtos) >= self.max_produtos:
                        break
                        
            except Exception as e:
                print(f"⚠️ Erro extraindo produto: {e}")
                continue
        
        return produtos
    
    async def _scroll_page(self, page):
        """Rola a página para carregar conteúdo dinâmico"""
        try:
            await page.evaluate("""
                window.scrollTo({
                    top: document.body.scrollHeight,
                    behavior: 'smooth'
                });
            """)
            await asyncio.sleep(2)
        except:
            # Fallback para scroll simples
            await page.mouse.wheel(0, 1000)
            await asyncio.sleep(2)
    
    async def _extrair_produto(self, elemento) -> Optional[ProdutoAmazon]:
        """Extrai dados de um elemento de produto"""
        
        # ASIN
        asin = await elemento.get_attribute("data-asin")
        if not asin or len(asin.strip()) == 0:
            return None
        
        # Título
        titulo = await self._extrair_titulo(elemento)
        if not titulo:
            titulo = "Produto Amazon"
        
        # Preço
        preco = await self._extrair_preco(elemento)
        
        # Imagem
        imagem = await self._extrair_imagem(elemento)
        
        # Link
        link = f"https://www.amazon.com.br/dp/{asin}?tag={self.store_id}"
        
        return ProdutoAmazon(
            asin=asin,
            titulo=titulo.strip()[:100],
            preco=preco,
            link=link,
            imagem=imagem
        )
    
    async def _extrair_titulo(self, elemento) -> Optional[str]:
        """Extrai o título do produto"""
        for seletor in self.selectors["titulo"]:
            try:
                el = await elemento.query_selector(seletor)
                if el:
                    return await el.inner_text()
            except:
                continue
        return None
    
    async def _extrair_preco(self, elemento) -> str:
        """Extrai o preço do produto"""
        for seletor in self.selectors["preco"]:
            try:
                el = await elemento.query_selector(seletor)
                if el:
                    texto = await el.inner_text()
                    if texto:
                        if "R$" in texto:
                            return texto.strip()
                        return f"R$ {texto.strip()}"
            except:
                continue
        return "Ver preço na Amazon"
    
    async def _extrair_imagem(self, elemento) -> Optional[str]:
        """Extrai a URL da imagem"""
        try:
            img = await elemento.query_selector(self.selectors["imagem"])
            if img:
                src = await img.get_attribute("src")
                if src:
                    # Tenta pegar imagem de maior qualidade
                    if "._" in src:
                        src = src.split("._")[0] + ".jpg"
                    return src
        except:
            pass
        return None

# Função de compatibilidade
async def minerar_amazon(urls: List[str], store_id: str) -> List[Dict[str, str]]:
    """Função de compatibilidade com o código existente"""
    miner = AmazonMiner(store_id)
    produtos = await miner.minerar(urls)
    return [p.to_dict() for p in produtos]