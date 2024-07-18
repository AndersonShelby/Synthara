#!/bin/bash

# Define a cor verde
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Função para exibir mensagens em verde
function green_echo() {
    echo -e "${GREEN}$1${NC}"
}

# Limpar a tela
clear

# Atualizando lista de pacotes
green_echo "Atualizando lista de pacotes..."
sudo apt update && sudo apt upgrade

# Instalar bibliotecas necessárias
green_echo "Instalando bibliotecas..."
pip install nltk scikit-learn

# Instalar sqlite3
green_echo "Instalando sqlite3..."
sudo apt-get install sqlite3

# Baixar recursos do NLTK
green_echo "Baixando recursos do NLTK..."
python3 -m nltk.downloader punkt
python3 -m nltk.downloader stopwords
python3 -m nltk.downloader wordnet

# Executar o script principal
green_echo "Executando o script principal..."
python3 Syn.py
