print("Carregando bibliotecas...")
import os
import time
import sqlite3
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

# Diretório onde este script está localizado
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')  # Diretório 'data' dentro do diretório principal

# Limpar console
os.system('clear')

print("Carregando recursos NLTK...")
# Baixar recursos NLTK
def baixar_recursos_nltk():
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')

baixar_recursos_nltk()


# Função para processar texto
def processar_texto(texto):
    tokens = word_tokenize(texto.lower())
    tokens = [t for t in tokens if t.isalnum()]
    tokens = [t for t in tokens if t not in stopwords.words('portuguese')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

# Função para carregar perguntas e respostas do SQLite
def carregar_perguntas_respostas_sqlite(nome_banco):
    db_path = os.path.join(DATA_DIR, nome_banco)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT pergunta, resposta FROM perguntas_respostas")
    perguntas_respostas = cursor.fetchall()
    conn.close()
    return {pergunta: resposta for pergunta, resposta in perguntas_respostas}

# Função para carregar perguntas e respostas do JSON
def carregar_perguntas_respostas_json(nome_arquivo):
    json_path = os.path.join(DATA_DIR, nome_arquivo)
    with open(json_path, 'r', encoding='utf-8') as f:
        perguntas_respostas = json.load(f)
    return perguntas_respostas

# Função para salvar perguntas e respostas no SQLite
def salvar_pergunta_resposta_sqlite(pergunta, resposta, nome_banco):
    db_path = os.path.join(DATA_DIR, nome_banco)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (?, ?)", (pergunta, resposta))
    conn.commit()
    conn.close()

# Função para salvar perguntas e respostas no JSON
def salvar_pergunta_resposta_json(pergunta, resposta, nome_arquivo):
    json_path = os.path.join(DATA_DIR, nome_arquivo)
    with open(json_path, 'r+', encoding='utf-8') as f:
        perguntas_respostas = json.load(f)
        perguntas_respostas[pergunta] = resposta
        f.seek(0)
        json.dump(perguntas_respostas, f, ensure_ascii=False, indent=4)

# Carregar perguntas e respostas de fontes externas
respostas_pre_definidas = {}

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
        return pergunta_similar, resposta
    else:
        return None, "Desculpe, eu não entendi a pergunta."

# Função para adicionar nova pergunta e resposta
def adicionar_nova_resposta(pergunta, resposta):
    salvar_pergunta_resposta_sqlite(pergunta, resposta, 'perguntas_respostas.db')
    salvar_pergunta_resposta_json(pergunta, resposta, 'perguntas_respostas.json')
    perguntas_bd.append(pergunta)
    perguntas_bd_processadas.append(processar_texto(pergunta))
    global perguntas_bd_vec
    perguntas_bd_vec = vectorizer.transform(perguntas_bd_processadas)
    respostas_pre_definidas[pergunta] = resposta

# Loop de interação contínua
os.system('clear')
while True:
    comando = input("Você: ").strip().lower()

    if comando == 'sair':
        print("Assistente: Até logo!")
        break
    elif comando == 'limpar':
        # Função para limpar o banco de dados (implemente conforme necessário)
        print("Comando 'limpar' não implementado.")
    elif comando == 'recriar':
        # Função para recriar o banco de dados (implemente conforme necessário)
        print("Comando 'recriar' não implementado.")
    else:
        pergunta_do_usuario = comando
        pergunta_similar, resposta = obter_resposta(pergunta_do_usuario)
        print(f"Assistente: {resposta}")
        
        if pergunta_similar:
            feedback = input("Essa resposta foi útil? (sim/não): ").strip().lower()
            if feedback == 'não':
                resposta_correta = input("Por favor, forneça a resposta correta: ").strip()
                adicionar_nova_resposta(pergunta_do_usuario, resposta_correta)
                print("Obrigado! Eu aprendi algo novo.")
        else:
            resposta_correta = input("Por favor, forneça a resposta correta: ").strip()
            adicionar_nova_resposta(pergunta_do_usuario, resposta_correta)
            print("Obrigado! Eu aprendi algo novo.")
