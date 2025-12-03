import streamlit as st
from googlesearch import search
from urllib.parse import urlparse
from collections import Counter
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
from search_helper import google_search_improved
from filter_engine import filter_search_results

# Configuração da página
st.set_page_config(
    page_title="Kairós- Rede de Livros",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS customizado para visual bonito
st.markdown("""
    <style>
        /* Paleta de cores elegante */
        :root {
            --primary: #2E7D32;
            --secondary: #1565C0;
            --accent: #F57C00;
            --bg-dark: #0F1419;
            --bg-light: #1A1F2E;
            --text-primary: #FFFFFF;
            --text-secondary: #B0BEC5;
        }
        
        /* Estilo geral */
        body {
            background: linear-gradient(135deg, #0F1419 0%, #1A1F2E 100%);
            color: var(--text-primary);
        }
        
        .stApp {
            background: linear-gradient(135deg, #0F1419 0%, #1A1F2E 100%);
        }
        
        /* Título principal */
        .main-title {
            text-align: center;
            font-size: 3.5em;
            font-weight: 900;
            color: #fff;
            margin-bottom: 0.5em;
           /*  text-shadow: 0 0 30px rgba(0, 150, 255, 0.6), 0 4px 15px rgba(196, 30, 58, 0.4); */
            letter-spacing: 2px;
        }
        
        .subtitle {
            text-align: center;
            color: var(--text-secondary);
            font-size: 1.2em;
            margin-bottom: 2em;
            font-weight: 300;
            letter-spacing: 1px;
        }
        
        /* Caixa de entrada */
        .search-container {
            background: linear-gradient(135deg, #1A2332 0%, #1F2937 100%);
            padding: 2em;
            border-radius: 15px;
            border: 2px solid rgba(46, 125, 50, 0.3);
            box-shadow: 0 8px 32px 0 rgba(46, 125, 50, 0.1);
            margin-bottom: 2em;
        }
        
        /* Labels */
        .stSelectbox label, .stTextInput label {
            color: var(--text-primary) !important;
            font-weight: 600 !important;
            font-size: 1.1em !important;
        }
        
        /* Input fields */
        .stSelectbox > div > div, .stTextInput > div > div {
            background: #0F1419 !important;
            border-color: rgba(46, 125, 50, 0.5) !important;
            border-radius: 10px !important;
        }
        
        .stSelectbox > div > div > select, .stTextInput input {
            color: var(--text-primary) !important;
            font-size: 1em !important;
        }
        
        /* Resultados */
        .results-container {
            background: linear-gradient(135deg, #1A2332 0%, #1F2937 100%);
            padding: 2em;
            border-radius: 15px;
            border: 2px solid rgba(21, 101, 192, 0.3);
            margin-top: 2em;
            box-shadow: 0 8px 32px 0 rgba(21, 101, 192, 0.1);
        }
        
        .result-link {
            background: #0F1419;
            padding: 1em;
            margin: 0.8em 0;
            border-radius: 10px;
            border-left: 4px solid #2E7D32;
            transition: all 0.3s ease;
        }
        
        .result-link:hover {
            border-left: 4px solid #F57C00;
            transform: translateX(5px);
            background: #1A1F2E;
        }
        
        .result-link a {
            color: #4DB8FF;
            text-decoration: none;
            word-break: break-all;
            font-weight: 500;
        }
        
        .result-link a:hover {
            color: #F57C00;
            text-decoration: underline;
        }
        
        /* Info box */
        .info-box {
            background: rgba(46, 125, 50, 0.1);
            border-left: 4px solid #2E7D32;
            padding: 1em;
            border-radius: 8px;
            margin: 1em 0;
            color: var(--text-secondary);
        }
        
        /* Gráficos */
        .chart-container {
            background: #0F1419;
            padding: 1.5em;
            border-radius: 12px;
            border: 1px solid rgba(46, 125, 50, 0.2);
        }
        
        /* Paginação */
        .stButton > button {
            background: linear-gradient(135deg, #2E7D32, #1565C0);
            color: white;
            border: none;
            padding: 0.8em 2em;
            border-radius: 25px;
            font-weight: 600;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(46, 125, 50, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(46, 125, 50, 0.5);
        }
        
        /* Subheadings */
        .stMarkdown h2 {
            color: var(--text-primary);
            border-bottom: 2px solid rgba(46, 125, 50, 0.3);
            padding-bottom: 0.5em;
            margin-top: 1.5em;
        }
        
        /* Dataframe */
        .stDataframe {
            background: #0F1419 !important;
        }
        
        .dataframe {
            background: #0F1419 !important;
            color: var(--text-primary) !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título e subtítulo
st.markdown('<div class="main-title">📚 Rizoma Kairós</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Buscador Inteligente de Livros com Dorks do Google</div>', unsafe_allow_html=True)

# Função wrapper para buscar com timeout
def google_search_safe(query, num_results=50):
    """Busca no Google com tratamento de erro e timeout"""
    try:
        # Tenta usar a função melhorada primeiro
        results = google_search_improved(query, num_results=num_results, sleep_interval=2)
        return results
    except Exception as e:
        st.error(f"Erro na busca: {str(e)[:100]}")
        return []

# Seção de busca com CSS
st.markdown("""
<style>
[data-testid="column"] {
    background: linear-gradient(135deg, #1A2332 0%, #1F2937 100%);
    padding: 2em;
    border-radius: 15px;
    border: 2px solid rgba(46, 125, 50, 0.3);
    box-shadow: 0 8px 32px 0 rgba(46, 125, 50, 0.1);
    margin-bottom: 2em;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    tipo_arquivo = st.selectbox(
        "📁 Tipo de arquivo",
        ["PDF", "EPUB", "DOCX", "MOBI", "TXT"],
        help="Selecione o formato do livro que deseja buscar"
    )

with col2:
    assunto = st.text_input(
        "🔍 Nome do livro ou autor",
        placeholder="Ex: O Cortiço - Aluísio Azevedo",
        help="Digite o nome do livro ou autor"
    )

# Montar a query
query = ""
if assunto:
    tipo_arquivo_lower = tipo_arquivo.lower()
    query = f'filetype:{tipo_arquivo_lower} {assunto}'

# Função para verificar se o link é válido
def is_valid_link(url):
    if "google.com/search?" in url or re.match(r"^https?://(?:www\.)?google\.com/", url):
        return False
    if not re.match(r"^https?://", url):
        return False
    return True

# Exibindo os resultados
RESULTADOS_POR_PAGINA = 10

if query:
    st.markdown(f"<div class='info-box'>🔎 <strong>Busca gerada:</strong> <code>{query}</code></div>", unsafe_allow_html=True)

    if 'todos_links' not in st.session_state or st.session_state.get('ultima_query') != query:
        try:
            with st.spinner("⏳ Buscando livros... isso pode levar um pouco..."):
                resultados = google_search_safe(query, num_results=50)
            
            # Aplicar engine de filtragem inteligente
            links_filtrados, stats = filter_search_results(resultados, min_score=0.3)
            
            st.session_state.todos_links = links_filtrados
            st.session_state.ultima_query = query
            st.session_state.pagina = 0
            st.session_state.filter_stats = stats
            
            if links_filtrados:
                st.success(f"✅ {len(links_filtrados)} resultados encontrados! (Bloqueados: {stats['blocked']} spam)")
            else:
                st.warning("⚠️ Nenhum resultado encontrado após filtros inteligentes. Tente outra busca.")
        except Exception as e:
            st.error(f"❌ Erro ao buscar: {e}")

    if 'todos_links' in st.session_state and st.session_state.todos_links:
        total = len(st.session_state.todos_links)
        inicio = st.session_state.pagina * RESULTADOS_POR_PAGINA
        fim = inicio + RESULTADOS_POR_PAGINA
        links_pagina = st.session_state.todos_links[inicio:fim]

        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        
        # Mostrar estatísticas de filtragem
        if 'filter_stats' in st.session_state:
            stats = st.session_state.filter_stats
            st.markdown(f"<div class='info-box'>🔍 <strong>Filtragem Inteligente:</strong> {stats['processed']} processados, {stats['blocked']} spam removido, {stats['filtered']} livros relevantes</div>", unsafe_allow_html=True)
        
        st.markdown(f"### 📖 Resultados da busca (página {st.session_state.pagina + 1} de {(total-1)//RESULTADOS_POR_PAGINA + 1})")
        
        for idx, url in enumerate(links_pagina, 1):
            st.markdown(f"""
            <div class="result-link">
                <strong>📎 Resultado {inicio + idx}:</strong><br>
                <a href="{url}" target="_blank">{url[:120]}...</a>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

        # Colunas para gráficos
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("🗺️ Top Domínios Encontrados")
            dominios = [urlparse(link).netloc for link in st.session_state.todos_links]
            contagem = Counter(dominios)
            df_dominios = pd.DataFrame(contagem.items(), columns=["Domínio", "Ocorrências"])
            df_dominios = df_dominios.sort_values(by="Ocorrências", ascending=False)
            st.dataframe(df_dominios.head(15), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            st.subheader("☁️ Nuvem de Palavras")
            palavras = [urlparse(link).netloc for link in st.session_state.todos_links]
            if palavras:
                texto = ' '.join(palavras)
                wordcloud = WordCloud(width=400, height=400, background_color='#0F1419', 
                                     colormap='viridis').generate(texto)
                fig, ax = plt.subplots(figsize=(5, 5))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                fig.patch.set_facecolor('#0F1419')
                st.pyplot(fig)
            st.markdown('</div>', unsafe_allow_html=True)

        # Paginação
        st.markdown("---")
        col3, col4 = st.columns(2)
        
        with col3:
            if st.session_state.pagina > 0:
                if st.button("⬅️ Página Anterior"):
                    st.session_state.pagina -= 1
                    st.rerun()

        with col4:
            if fim < total:
                if st.button("Próxima Página ➡️"):
                    st.session_state.pagina += 1
                    st.rerun()

