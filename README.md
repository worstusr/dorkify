# 📚 Dorkify - Buscador Inteligente de Livros

Um buscador visual e inteligente feito com Python + Streamlit + Selenium. O **Dorkify** usa Google Dorks para realizar buscas específicas como `filetype:pdf`, tudo sem depender de APIs, com visualização clara, interativa e design moderno.

---

## 🚀 Funcionalidades

✅ **Interface elegante e responsiva** - Design moderno com gradientes e animações  
✅ **Busca inteligente de arquivos** - Suporta PDF, EPUB, DOCX, MOBI, TXT  
✅ **Scraping com Selenium** - Utiliza Chrome headless para acesso real ao Google  
✅ **Nuvem de palavras dinâmica** - Visualização dos domínios mais frequentes  
✅ **Tabela de domínios** - Top 15 domínios encontrados com contagem  
✅ **Paginação de resultados** - Navegação fácil entre páginas  
✅ **Links clicáveis** - Acesso direto aos arquivos encontrados  
✅ **Logs em tempo real** - Debug completo das buscas  

---

## 📖 Exemplos de uso

- Buscar livros em PDF: **"O Cortiço - Aluísio Azevedo"**
- Encontrar e-books: **"Harry Potter"**
- Descobrir documentos técnicos: **"Machine Learning"**
- Buscar teses e dissertações por tema

---

## 💻 Requisitos do Sistema

- Python 3.10+
- Google Chrome instalado
- pip (gerenciador de pacotes Python)

---

## ⚙️ Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/worstusr/dorkify.git
cd dorkify
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

**Nota:** A primeira execução vai baixar automaticamente o ChromeDriver via webdriver-manager.

### 3. Execute a aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em: `http://localhost:8501`

---

## 📦 Dependências

- **streamlit** - Framework web para Python
- **selenium** - Automação de navegador
- **webdriver-manager** - Gerenciamento automático do ChromeDriver
- **pandas** - Análise de dados
- **matplotlib** - Visualização
- **wordcloud** - Geração de nuvem de palavras
- **googlesearch-python** - Suporte adicional de busca

---

## 🎨 Design & UI

A interface foi redesenhada com:
- **Paleta de cores profissional** - Verde, azul e laranja em gradientes elegantes
- **Tema escuro otimizado** - Reduz cansaço visual
- **Animações suaves** - Transições ao interagir com resultados
- **Responsividade completa** - Funciona em desktop e tablet

---

## 🔍 Como funciona

1. Selecione o tipo de arquivo (PDF, EPUB, DOCX, MOBI ou TXT)
2. Digite o nome do livro ou autor
3. A ferramenta converte em um Google Dork: `filetype:pdf Nome do Livro`
4. Selenium abre Chrome e executa a busca
5. Resultados são extraídos e exibidos com análise de domínios

---

## ⚠️ Notas Importantes

- **Google pode bloquear buscas frequentes** - Use intervalos entre buscas
- **Respeite os termos de serviço** - Use responsavelmente
- **Verificar direitos autorais** - Sempre respeite copyright
- **Primeira busca pode ser lenta** - Chrome precisa inicializar

---

## 🐛 Troubleshooting

**Erro: "Chrome não encontrado"**
```bash
# Linux/Fedora
sudo dnf install google-chrome-stable

# Ubuntu/Debian
sudo apt-get install google-chrome-stable

# macOS
brew install --cask google-chrome
```

**Erro: "Nenhum resultado encontrado"**
- Tente uma busca mais geral
- Verifique sua conexão com a internet
- Aguarde alguns minutos e tente novamente

---

## 📝 Licença

MIT License - Veja o arquivo LICENSE para detalhes

---

## 🤝 Contribuições

Contribuições são bem-vindas! Para reportar bugs ou sugerir melhorias, abra uma issue no GitHub.
