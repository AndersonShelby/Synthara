# Synthara v1 PROTÓTIPO

**Instalação:**
*   Use `sudo apt install git` para instalar o git.
*   Use `https://github.com/AndersonShelby/Synthara.git` para clonar o repositório.
*   Use `chmod +x setup.sh` para dar autorização para executar o script, e, em seguida use `bash setup.sh` para instalar as bibliotecas necessárias e executar o script principal.


# Assistente de Texto com NLP

Este projeto é um assistente de texto simples que utiliza Processamento de Linguagem Natural (NLP) para responder às perguntas dos usuários. O assistente pode aprender novas perguntas e respostas ao longo do tempo, armazenando-as em um banco de dados SQLite e em um arquivo JSON.

## Funcionalidades

- **Processamento de Linguagem Natural:** Tokenização, remoção de stopwords e lematização.
- **Similaridade de Texto:** Utilização de vetorização e similaridade de cosseno para encontrar respostas apropriadas.
- **Interação Contínua:** Loop contínuo para interação com o usuário até que ele decida sair.
- **Aprendizado Contínuo:** Capacidade de aprender novas perguntas e respostas fornecidas pelo usuário.

## Dependências

### O projeto depende das seguintes bibliotecas:

- `os`
- `nltk`
- `time`
- `sqlite3`
- `json`
- `sklearn`

### Você pode instalar as dependências do `nltk` executando:

```python
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

## Estrutura do Código

### Importação de Bibliotecas e Configuração Inicial

```python
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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
```

### Baixar Recursos NLTK

```python
def baixar_recursos_nltk():
    nltk.download('punkt_tab')
    nltk.download('stopwords')
    nltk.download('wordnet')

baixar_recursos_nltk()
```

### Processamento de Texto

```python
def processar_texto(texto):
    tokens = word_tokenize(texto.lower())
    tokens = [t for t in tokens if t.isalnum()]
    tokens = [t for t in tokens if t not in stopwords.words('portuguese')]
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)
```

### Carregamento e Salvamento de Perguntas e Respostas

#### Carregar Perguntas e Respostas do SQLite

```python
def carregar_perguntas_respostas_sqlite(nome_banco):
    db_path = os.path.join(DATA_DIR, nome_banco)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT pergunta, resposta FROM perguntas_respostas")
    perguntas_respostas = cursor.fetchall()
    conn.close()
    return {pergunta: resposta for pergunta, resposta in perguntas_respostas}
```

#### Carregar Perguntas e Respostas do JSON

```python
def carregar_perguntas_respostas_json(nome_arquivo):
    json_path = os.path.join(DATA_DIR, nome_arquivo)
    with open(json_path, 'r', encoding='utf-8') as f:
        perguntas_respostas = json.load(f)
    return perguntas_respostas
```

#### Salvar Perguntas e Respostas no SQLite

```python
def salvar_pergunta_resposta_sqlite(pergunta, resposta, nome_banco):
    db_path = os.path.join(DATA_DIR, nome_banco)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (?, ?)", (pergunta, resposta))
    conn.commit()
    conn.close()
```

#### Salvar Perguntas e Respostas no JSON

```python
def salvar_pergunta_resposta_json(pergunta, resposta, nome_arquivo):
    json_path = os.path.join(DATA_DIR, nome_arquivo)
    with open(json_path, 'r+', encoding='utf-8') as f:
        perguntas_respostas = json.load(f)
        perguntas_respostas[pergunta] = resposta
        f.seek(0)
        json.dump(perguntas_respostas, f, ensure_ascii=False, indent=4)
```

### Inicialização e Carregamento de Dados

```python
respostas_pre_definidas = {}

try:
    respostas_sqlite = carregar_perguntas_respostas_sqlite('perguntas_respostas.db')
    respostas_pre_definidas.update(respostas_sqlite)
except Exception as e:
    print(f"Erro ao carregar banco de dados SQLite: {e}")

try:
    respostas_json = carregar_perguntas_respostas_json('perguntas_respostas.json')
    respostas_pre_definidas.update(respostas_json)
except Exception as e:
    print(f"Erro ao carregar arquivo JSON: {e}")
```

### Pré-processamento de Perguntas e Vetorização

```python
perguntas_bd = list(respostas_pre_definidas.keys())
perguntas_bd_processadas = [processar_texto(p) for p in perguntas_bd]

vectorizer = CountVectorizer().fit(perguntas_bd_processadas)
perguntas_bd_vec = vectorizer.transform(perguntas_bd_processadas)
```

### Obtenção de Respostas

```python
def obter_resposta(pergunta):
    pergunta_processada = processar_texto(pergunta)
    print("Carregando...")
    time.sleep(1)
    pergunta_vec = vectorizer.transform([pergunta_processada])
    similaridades = cosine_similarity(pergunta_vec, perguntas_bd_vec).flatten()
    max_similaridade = similaridades.max()

    if max_similaridade >= 0.2:
        idx_pergunta_similar = similaridades.argmax()
        pergunta_similar = perguntas_bd[idx_pergunta_similar]
        resposta = respostas_pre_definidas[pergunta_similar]
        return pergunta_similar, resposta
    else:
        return None, "Desculpe, eu não entendi a pergunta."
```

### Adição de Novas Perguntas e Respostas

```python
def adicionar_nova_resposta(pergunta, resposta):
    salvar_pergunta_resposta_sqlite(pergunta, resposta, 'perguntas_respostas.db')
    salvar_pergunta_resposta_json(pergunta, resposta, 'perguntas_respostas.json')
    perguntas_bd.append(pergunta)
    perguntas_bd_processadas.append(processar_texto(pergunta))
    global perguntas_bd_vec
    perguntas_bd_vec = vectorizer.transform(perguntas_bd_processadas)
    respostas_pre_definidas[pergunta] = resposta
```

### Interação com o Usuário

```python
while True:
    comando = input("Você: ").strip().lower()

    if comando == 'sair':
        print("Assistente: Até logo!")
        break
    elif comando == 'limpar':
        print("Comando 'limpar' não implementado.")
    elif comando == 'recriar':
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
```

## Resumo do Funcionamento

1. **Inicialização:** O script baixa recursos NLTK e carrega perguntas e respostas de um banco de dados SQLite e um arquivo JSON.
2. **Processamento:** Quando o usuário faz uma pergunta, ela é processada (tokenização, remoção de stopwords, lematização).
3. **Vetorização:** A pergunta do usuário é vetorizada e comparada com perguntas pré-processadas usando similaridade de cosseno.
4. **Resposta:** Se a similaridade for suficiente, a resposta correspondente é retornada. Caso contrário, o usuário é solicitado a fornecer uma resposta correta, que é então armazenada no banco de dados e no arquivo JSON para uso futuro.
5. **Interação:** O loop contínuo permite a interação constante até que o usuário decida sair.
