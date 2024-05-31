print("Carregando bibliotecas...")
import nltk
import os
import time
import sqlite3
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

os.system('clear')
print("Carregando recursos NLTK...")
# Função para baixar pacotes necessários do NLTK
def baixar_recursos_nltk():
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Baixar recursos do NLTK
baixar_recursos_nltk()

# Função para processamento de texto
def processar_texto(texto):
    tokens = word_tokenize(texto.lower())
    tokens = [t for t in tokens if t.isalnum()]
    tokens = [t for t in tokens if t not in stopwords.words('portuguese')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

# Função para carregar perguntas e respostas de um banco de dados SQLite
def carregar_perguntas_respostas_sqlite(nome_banco):
    conn = sqlite3.connect(nome_banco)
    cursor = conn.cursor()
    cursor.execute("SELECT pergunta, resposta FROM perguntas_respostas")
    perguntas_respostas = cursor.fetchall()
    conn.close()
    return {pergunta: resposta for pergunta, resposta in perguntas_respostas}

# Função para carregar perguntas e respostas de um arquivo JSON
def carregar_perguntas_respostas_json(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as f:
        perguntas_respostas = json.load(f)
    return perguntas_respostas

# Banco de dados de perguntas e respostas predefinidas
respostas_pre_definidas = {
    "Qual é o seu nome?": "Meu nome é Genie.",
    "Como você está?": "Eu não tenho sentimentos, mas estou aqui para ajudar!",
    "O que você faz?": "Eu sou um modelo de linguagem treinado para responder às suas perguntas.",
    "Quem te criou?": "Fui criado por um desenvolvedor apaixonado por inteligência artificial.",
    "Qual a sua cor favorita?": "Não tenho percepção de cor, mas posso ser qualquer cor que você preferir!",
}

# Atualizar respostas predefinidas com as respostas do banco de dados SQLite
try:
    respostas_sqlite = carregar_perguntas_respostas_sqlite('perguntas_respostas.db')
    respostas_pre_definidas.update(respostas_sqlite)
except Exception as e:
    print(f"Erro ao carregar banco de dados SQLite: {e}")

# Atualizar respostas predefinidas com as respostas do arquivo JSON
try:
    respostas_json = carregar_perguntas_respostas_json('perguntas_respostas.json')
    respostas_pre_definidas.update(respostas_json)
except Exception as e:
    print(f"Erro ao carregar arquivo JSON: {e}")

# Pré-processamento das perguntas do banco de dados
perguntas_bd = list(respostas_pre_definidas.keys())
perguntas_bd_processadas = [processar_texto(p) for p in perguntas_bd]

# Criar o vetorizador uma vez fora do loop
vectorizer = CountVectorizer().fit(perguntas_bd_processadas)
perguntas_bd_vec = vectorizer.transform(perguntas_bd_processadas)

# Limiar mínimo de similaridade
limiar_similaridade = 0.2

# Função para obter resposta
def obter_resposta(pergunta):
    pergunta_processada = processar_texto(pergunta)
    
    print("Carregando...")
    time.sleep(1)

    # Vetorizar a pergunta do usuário
    pergunta_vec = vectorizer.transform([pergunta_processada])

    # Calcular similaridade de cosseno entre a pergunta do usuário e as perguntas no banco de dados
    similaridades = cosine_similarity(pergunta_vec, perguntas_bd_vec).flatten()

    # Encontrar a maior similaridade
    max_similaridade = similaridades.max()

    # Verificar se a maior similaridade está acima do limiar mínimo
    if max_similaridade >= limiar_similaridade:
        idx_pergunta_similar = similaridades.argmax()
        pergunta_similar = perguntas_bd[idx_pergunta_similar]
        resposta = respostas_pre_definidas[pergunta_similar]
        return f"Assistente: {resposta}"
    else:
        return "Assistente: Desculpe, eu não entendi a pergunta."

# Loop de interação contínua
os.system('clear')
while True:
    pergunta_do_usuario = input("Você: ")

    # Verifica se o usuário deseja sair
    if pergunta_do_usuario.lower() == 'sair':
        print("Assistente: Até logo!")
        break

    resposta = obter_resposta(pergunta_do_usuario)
    print(resposta)