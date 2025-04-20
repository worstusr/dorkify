# dorkify
Este buscador nasceu de uma ideia de análise visual: Combinar dorks com visualizações, como nuvem de palavras e distribuição de domínios, para gerar insights rápidos sobre a web — direto no seu navegador. Simples, rápido, escalável e sem dependência de APIs externas.

 🔍 Buscador Dorks Inteligente

Um buscador simples, direto e visual feito com Python + Streamlit. Ele utiliza dorks do Google para realizar buscas específicas como `filetype:pdf`, `site:gov.br` e muito mais — sem necessidade de API ou autenticação.

___

 🚀 Funcionalidades

✅ Interface interativa com Streamlit  
✅ Busca com dorks personalizadas  
✅ Filtros inteligentes e navegação por páginas  
✅ Nuvem de palavras dos domínios mais frequentes  
✅ Gráfico visual com distribuição dos resultados  
✅ Tudo em um único arquivo (`app.py`)

___

 💡 Exemplo de uso

- Buscar arquivos PDF sobre "orçamento 2024"
- Explorar resultados de sites específicos, como `site:unesp.br`
- Identificar padrões e domínios mais presentes visualmente

___

 ⚙️ Como rodar

bash
git clone https://github.com/seu-usuario/buscador-dorks-inteligente.git
cd buscador-dorks-inteligente

pip install -r requirements.txt

streamlit run app.py
