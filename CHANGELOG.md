# 📝 CHANGELOG

## [2.0.0] - 2025-12-03

### ✨ Novo

- **Scraping com Selenium** - Implementado Chrome headless para acesso real ao Google Search
- **Design UI completamente renovado** - Paleta de cores profissional com gradientes
- **CSS customizado** - Tema escuro elegante com animações suaves
- **Suporte a múltiplos formatos** - PDF, EPUB, DOCX, MOBI, TXT
- **Nuvem de palavras dinâmica** - Visualização de padrões nos domínios
- **Tabela de análise de domínios** - Top 15 domínios encontrados
- **Novo arquivo helper** - `search_helper.py` com lógica de Selenium

### 🔧 Corrigido

- ✅ Resolvido problema de bloqueio do Google
- ✅ Corrigida incompatibilidade com altair/Python 3.14
- ✅ Melhorado tratamento de erros na busca
- ✅ Paginação agora funciona corretamente

### 📦 Dependências Atualizadas

```
streamlit>=1.28.0
googlesearch-python>=1.3.0
wordcloud>=1.9.0
matplotlib>=3.7.0
pandas>=2.0.0
selenium>=4.0.0
webdriver-manager>=4.0.0
```

### 🎨 Melhorias de UX

- Interface simplificada apenas com busca de arquivos
- Indicadores visuais melhorados (emojis e cores)
- Buttons com gradientes e hover effects
- Info boxes com design coeso
- Responsividade melhorada

### 📚 Documentação

- README completamente reescrito
- Adicionado guia de instalação
- Troubleshooting section
- Exemplos de uso

---

## [1.0.0] - 2024-XX-XX

### ✨ Funcionalidades Iniciais

- Busca com Google Dorks
- Interface Streamlit básica
- Paginação de resultados
- Visualização de domínios
- Suporte a diferentes tipos de busca
