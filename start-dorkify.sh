#!/bin/bash

# Script para iniciar Dorkify com Streamlit + NGrok
# Inicia em background e salva o link público

cd /home/iawsec/Documents/anon_antifa/dorkify

# Inicia Streamlit
/home/iawsec/.local/bin/streamlit run app.py --server.port=8501 --server.address=127.0.0.1 > /tmp/streamlit.log 2>&1 &
STREAMLIT_PID=$!

# Aguarda Streamlit iniciar
sleep 5

# Inicia NGrok e captura o link
NGROK_OUTPUT=$(/usr/local/bin/ngrok http 8501 --log=stdout 2>&1)

# Extrai o link público e salva
echo "$NGROK_OUTPUT" | grep "url=" | grep "https" | head -1 | sed 's/.*url=//;s/ .*//' > /tmp/dorkify-link.txt

# Mantém os processos rodando
wait $STREAMLIT_PID
