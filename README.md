# 🔍 dorkfy

Um buscador visual e inteligente feito com Python + Streamlit. O `dorkfy` usa dorks do Google para realizar buscas específicas como `filetype:pdf`, `site:gov.br`, e muito mais — tudo sem depender de APIs, com visualização clara e interativa.

---

## 🚀 Funcionalidades

✅ Interface interativa com Streamlit  
✅ Sugestões e uso de dorks inteligentes  
✅ Nuvem de palavras com domínios mais frequentes  
✅ Visualização dos domínios encontrados em gráfico  
✅ Paginação dos resultados  
✅ Código enxuto, em um único arquivo (`app.py`)

---

## 💡 Exemplos de uso

- Buscar arquivos PDF sobre "orçamento 2024"
- Encontrar apresentações `.pptx` sobre tecnologia
- Navegar por resultados de domínios específicos, como `site:unesp.br`

---

## ⚙️ Como rodar

```bash
git clone https://github.com/seu-usuario/dorkfy.git
cd dorkfy

pip install -r requirements.txt

streamlit run app.py
