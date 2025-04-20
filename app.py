import streamlit as st
from googlesearch import search
from urllib.parse import urlparse
from collections import Counter
import pandas as pd
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="Buscador Inteligente", layout="wide")
st.title("🔍 Buscador Inteligente com Dorks")

# Tipo de busca
tipo = st.radio("O que você está procurando?", ["Arquivo", "Site específico", "Outro"])
query = ""

# Montando a query conforme o tipo de busca
if tipo == "Arquivo":
    tipo_arquivo = st.selectbox("Tipo de arquivo", ["pdf", "docx", "xlsx", "pptx", "txt"])
    assunto = st.text_input("Assunto ou palavra-chave", placeholder="ex: orçamento 2024")
    if assunto:
        query = f'filetype:{tipo_arquivo} {assunto}'

elif tipo == "Site específico":
    site = st.text_input("Site ou domínio (ex: gov.br)", placeholder="ex: gov.br")
    assunto = st.text_input("Assunto ou palavra-chave", placeholder="ex: covid vacinação")
    if site and assunto:
        query = f'site:{site} {assunto}'

else:
    query = st.text_input("Escreva sua busca diretamente")

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
    st.markdown(f"**Busca gerada:** `{query}`")
    st.divider()

    if 'todos_links' not in st.session_state or st.session_state.get('ultima_query') != query:
        try:
            resultados = search(query, num_results=50)
            links_filtrados = [url for url in resultados if is_valid_link(url)]
            st.session_state.todos_links = links_filtrados
            st.session_state.ultima_query = query
            st.session_state.pagina = 0
        except Exception as e:
            st.error(f"Erro ao buscar: {e}")

    if 'todos_links' in st.session_state:
        total = len(st.session_state.todos_links)
        inicio = st.session_state.pagina * RESULTADOS_POR_PAGINA
        fim = inicio + RESULTADOS_POR_PAGINA
        links_pagina = st.session_state.todos_links[inicio:fim]

        st.subheader(f"🌐 Resultados da busca (página {st.session_state.pagina + 1})")
        palavras = []

        for url in links_pagina:
            st.write(f"🔗 [{url}]({url})")
            palavras.append(urlparse(url).netloc)

        # Organizando o layout com colunas
        col1, col2 = st.columns([3, 1])  # A primeira coluna maior e a segunda para a nuvem de palavras

        with col1:
            st.subheader("🗺️ Mapa de domínios encontrados")
            dominios = [urlparse(link).netloc for link in st.session_state.todos_links]
            contagem = Counter(dominios)
            df_dominios = pd.DataFrame(contagem.items(), columns=["Domínio", "Ocorrências"])
            df_dominios = df_dominios.sort_values(by="Ocorrências", ascending=False)
            st.bar_chart(df_dominios.set_index("Domínio"))

        with col2:
            st.subheader("🌐 Nuvem de palavras dos resultados")
            if palavras:
                texto = ' '.join(palavras)
                wordcloud = WordCloud(width=400, height=400, background_color='white').generate(texto)
                fig, ax = plt.subplots(figsize=(4, 4))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)

        col3, col4 = st.columns(2)
        with col3:
            if st.session_state.pagina > 0:
                if st.button("⬅️ Página anterior"):
                    st.session_state.pagina -= 1
                    st.rerun()

        with col4:
            if fim < total:
                if st.button("➡️ Próxima página"):
                    st.session_state.pagina += 1
                    st.rerun()

