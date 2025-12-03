"""
Filtering Engine para Dorkify
Engine inteligente de filtragem de resultados de busca
Garante que apenas URLs relevantes (livros) sejam retornadas
"""

import re
from urllib.parse import urlparse, unquote
from typing import List, Dict, Tuple


class FilterEngine:
    """
    Engine responsável por filtrar e ranquear resultados de busca.
    Remove spam, valida domínios e classifica relevância.
    """

    # Domínios BLOQUEADOS (spam, mapas, redes sociais, etc)
    BLACKLIST_DOMAINS = {
        'maps.google.com',
        'google.com/maps',
        'reddit.com',
        'twitter.com',
        'facebook.com',
        'instagram.com',
        'tiktok.com',
        'pinterest.com',
        'linkedin.com',
        'youtube.com',
        'youtu.be',
        'amazon.com',  # Vendas, não downloads
        'amazon.com.br',
        'ebay.com',
        'alibaba.com',
        'github.com/raw',  # Scripts raw, não livros
        'pastebin.com',
        'stackoverflow.com',
        'quora.com',
        'medium.com',
        'wordpress.com',
        'blogspot.com',
        'tumblr.com',
        'flickr.com',
        'vimeo.com',
        'dailymotion.com',
        'soundcloud.com',
        'spotify.com',
        'discord.com',
        'telegram.org',
        'whatsapp.com',
        'alibaba',
        'ebay',
        'amazon',
    }

    # Domínios CONFIÁVEIS (bibliotecas digitais, arquivos)
    WHITELIST_DOMAINS = {
        'archive.org',
        'openlibrary.org',
        'project-gutenberg.org',
        'gutenberg.org',
        'standard-ebooks.org',
        'smashwords.com',  # E-books legais
        'leanpub.com',
        'wattpad.com',
        'issuu.com',
        'scribd.com',
        'pdfdrive.com',
        'pdfbooksworld.com',
        'bookzz.org',
        'b-ok.org',
        'libgen.rs',
        'libgen.is',
        'libgen.io',
        'libgen.me',
        'sci-hub.se',
        'sci-hub.st',
        'universitypress.org',
        'open.ac.uk',  # Universidade aberta (UK)
        'muse.jhu.edu',
        'jstor.org',
        'doi.org',
        'arxiv.org',
        'researchgate.net',
        'academia.edu',
        'semanticscholar.org',
        'springeropen.com',
        'mdpi.com',
        'brill.com',
        'degruyter.com',
        'landesarchiv',  # Arquivos regionais (Alemanho)
        'historia.org.br',
        'bn.br',  # Biblioteca Nacional Brasil
        'bibliotecas.uncuyo.edu.ar',  # Universidades Argentina
        'edu.ar',  # Domínio educacional Argentina
    }

    # Extensões de arquivo PERMITIDAS
    ALLOWED_EXTENSIONS = {
        '.pdf', '.epub', '.docx', '.doc', '.mobi', '.txt',
        '.azw', '.azw3', '.ibooks', '.cbz', '.cbr',
    }

    # Padrões de URL que indicam spam/redirect
    SPAM_PATTERNS = [
        r'adchoices',
        r'pagead',
        r'doubleclick',
        r'googleadservices',
        r'linksynergy',
        r'shareasale',
        r'amazon-adsystem',
        r'facebook.com/sharer',
        r'pinterest.com/pin',
        r'malware',
        r'virus',
        r'crack',
        r'keygen',
    ]

    def __init__(self):
        """Inicializa o engine de filtragem"""
        self.blocked_count = 0
        self.processed_count = 0

    def is_blacklisted(self, url: str) -> bool:
        """
        Verifica se domínio está na blacklist
        Retorna True se deve bloquear
        """
        try:
            domain = urlparse(url).netloc.lower()
            
            # Remove www.
            if domain.startswith('www.'):
                domain = domain[4:]
            
            # Verificar blacklist exata
            if domain in self.BLACKLIST_DOMAINS:
                return True
            
            # Verificar blacklist parcial (subdomains)
            for blocked in self.BLACKLIST_DOMAINS:
                if domain.endswith('.' + blocked) or domain == blocked:
                    return True
            
            return False
        except:
            return True

    def is_whitelisted(self, url: str) -> bool:
        """
        Verifica se domínio está na whitelist (confiável)
        Retorna True se é fonte confiável
        """
        try:
            domain = urlparse(url).netloc.lower()
            
            if domain.startswith('www.'):
                domain = domain[4:]
            
            for whitelisted in self.WHITELIST_DOMAINS:
                if domain.endswith('.' + whitelisted) or domain == whitelisted:
                    return True
            
            return False
        except:
            return False

    def has_spam_pattern(self, url: str) -> bool:
        """
        Detecta padrões de spam/ads na URL
        """
        url_lower = url.lower()
        for pattern in self.SPAM_PATTERNS:
            if pattern in url_lower:
                return True
        return False

    def has_valid_extension(self, url: str) -> bool:
        """
        Valida se URL provavelmente aponta para arquivo de livro
        """
        # Tira parâmetros da URL
        path = urlparse(url).path.lower()
        
        # Se não tem extensão óbvia, assume que pode ser OK
        # (alguns servidores servem PDFs sem extensão)
        if not any(path.endswith(ext) for ext in self.ALLOWED_EXTENSIONS):
            # Mas se tem extensão, deve ser válida
            if '.' in path.split('/')[-1]:
                return False
        
        return True

    def calculate_score(self, url: str) -> float:
        """
        Calcula score de relevância (0.0 - 1.0)
        Quanto maior, mais provável que seja um livro real
        """
        score = 0.5  # Score base
        
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            
            # Whitelist: +0.4 pontos
            if self.is_whitelisted(url):
                score += 0.4
            
            # Padrões de livros no nome do arquivo
            if any(indicator in path for indicator in [
                'book', 'ebook', 'novel', 'pdf', 'epub', 'mobi',
                'calibre', 'literatura', 'obra', 'author'
            ]):
                score += 0.2
            
            # URL com estrutura clara (não redirect chain)
            if len(parsed.query) == 0 or len(parsed.query) < 100:
                score += 0.1
            
            # Domínio educacional
            if any(edu in domain for edu in ['.edu', '.ac.', 'university', 'library', 'arquivo']):
                score += 0.15
            
            # Penalidades
            if self.has_spam_pattern(url):
                score -= 0.3
            
            if not self.has_valid_extension(url):
                score -= 0.2
            
            # Clamp entre 0 e 1
            return max(0.0, min(1.0, score))
        
        except:
            return 0.3  # Score baixo em caso de erro

    def filter_results(
        self,
        urls: List[str],
        min_score: float = 0.3
    ) -> List[Dict[str, any]]:
        """
        Filtra e ranqueia lista de URLs
        
        Args:
            urls: Lista de URLs brutas do Selenium
            min_score: Score mínimo para incluir resultado (0.0-1.0)
        
        Returns:
            Lista de dicts com URL, score e reasoning
        """
        filtered_results = []
        self.processed_count = 0
        self.blocked_count = 0
        
        for url in urls:
            self.processed_count += 1
            
            # Validações básicas
            if not url or not url.startswith(('http://', 'https://')):
                continue
            
            # Bloquear blacklist
            if self.is_blacklisted(url):
                self.blocked_count += 1
                continue
            
            # Calcular score
            score = self.calculate_score(url)
            
            # Aplicar threshold
            if score < min_score:
                continue
            
            # Determinar reasoning
            reasons = []
            if self.is_whitelisted(url):
                reasons.append('whitelist')
            if 'book' in url.lower() or 'ebook' in url.lower():
                reasons.append('book_indicator')
            if '.edu' in url or '.ac.' in url:
                reasons.append('academic')
            
            filtered_results.append({
                'url': url,
                'score': round(score, 2),
                'reasons': reasons or ['generic_domain']
            })
        
        # Ordenar por score (descendente)
        filtered_results.sort(key=lambda x: x['score'], reverse=True)
        
        return filtered_results

    def get_stats(self) -> Dict[str, int]:
        """
        Retorna estatísticas da filtragem
        """
        return {
            'processed': self.processed_count,
            'blocked': self.blocked_count,
            'allowed': self.processed_count - self.blocked_count
        }


# Função wrapper para uso fácil
def filter_search_results(
    urls: List[str],
    min_score: float = 0.3
) -> Tuple[List[str], Dict[str, int]]:
    """
    Interface simples para filtrar resultados
    
    Args:
        urls: Lista de URLs
        min_score: Score mínimo (0.3 = moderado, 0.5 = rigoroso)
    
    Returns:
        Tupla (urls_filtradas_ordenadas, estatísticas)
    """
    engine = FilterEngine()
    results = engine.filter_results(urls, min_score=min_score)
    
    filtered_urls = [r['url'] for r in results]
    stats = engine.get_stats()
    stats['filtered'] = len(filtered_urls)
    
    return filtered_urls, stats
