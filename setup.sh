#!/bin/bash

# Instalar bibliotecas necessárias
echo "Instalando bibliotecas..."
pip install nltk scikit-learn

# Instalar sqlite3
echo "Instalando sqlite3..."
sudo apt-get install sqlite3

# Baixar recursos do NLTK
echo "Baixando recursos do NLTK..."
python -m nltk.downloader punkt
python -m nltk.downloader stopwords
python -m nltk.downloader wordnet

# Executar o script principal
echo "Executando o script principal..."
python Genie.py
