"""Helper para buscar no Google usando Selenium com Chrome headless"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def google_search_improved(query, num_results=50, sleep_interval=1):
    """
    Busca no Google usando Selenium com Chrome headless
    Funciona porque executa JavaScript, diferente de requisições HTTP simples
    """
    
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36')
    
    results = []
    driver = None
    
    try:
        print(f"[SELENIUM] Inicializando Chrome...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"[SELENIUM] Acessando Google com query: {query}")
        driver.get(f'https://www.google.com/search?q={query}')
        
        # Espera os resultados carregarem
        print(f"[SELENIUM] Aguardando resultados...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href*="/url?q="]'))
        )
        
        print(f"[SELENIUM] Extraindo links...")
        
        # Scroll para carregar mais resultados
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while len(results) < num_results:
            # Encontra todos os links
            links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/url?q="]')
            print(f"[SELENIUM] Links encontrados: {len(links)}")
            
            for link in links:
                if len(results) >= num_results:
                    break
                    
                href = link.get_attribute('href')
                if href and '/url?q=' in href:
                    try:
                        # Extrai URL real
                        url = href.split('/url?q=')[1].split('&')[0]
                        if url and url not in results and not url.startswith('webcache'):
                            results.append(url)
                            print(f"[SELENIUM] Link {len(results)}: {url[:80]}")
                    except:
                        continue
            
            if len(results) >= num_results:
                break
            
            # Scroll para carregar mais
            print(f"[SELENIUM] Scrollando para mais resultados...")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(sleep_interval)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print(f"[SELENIUM] Fim da página atingido")
                break
            last_height = new_height
        
        print(f"[SELENIUM] Total de resultados: {len(results)}")
        return results
        
    except Exception as e:
        print(f"[SELENIUM] ERRO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return results
        
    finally:
        if driver:
            print(f"[SELENIUM] Fechando browser")
            driver.quit()
