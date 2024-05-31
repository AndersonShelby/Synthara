import sqlite3
import wikipediaapi

# Definir o agente de usuário
USER_AGENT = "MyWikiBot/1.0 (https://example.com/contact; myemail@example.com)"

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('informacoes_wikipedia.db')
cursor = conn.cursor()

# Criar a tabela no banco de dados, se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS informacoes_wikipedia (
    titulo TEXT,
    conteudo TEXT
)
''')

# Títulos de exemplo para buscar informações na Wikipédia
titulos = [
    "Marte",
    "Lua",
    "Sistema Solar",
    "Albert Einstein",
    "Inteligência Artificial",
    "Python (linguagem de programação)",
    "História da computação",
    "Teoria da relatividade",
    "Mecânica quântica",
    "Buracos negros",
    "Evolução",
    "Genética",
    "Clima",
    "Biodiversidade",
    "Energias renováveis",
    "Matemática",
    "Física",
    "Química",
    "Biologia",
    "Astronomia",
    "Geografia",
    "História",
    "Economia",
    "Psicologia",
    "Filosofia",
    "Sociologia",
    "Antropologia",
    "Literatura",
    "Arte",
    "Música",
    "Cinema",
    "Fotografia",
    "Engenharia",
    "Arquitetura",
    "Medicina",
    "Enfermagem",
    "Farmácia",
    "Direito",
    "Administração",
    "Educação",
    "Pedagogia",
    "Esportes",
    "Tecnologia da Informação",
    "Redes de Computadores",
    "Segurança da Informação",
    "Inteligência Coletiva",
    "Robótica",
    "Automação",
    "Indústria 4.0",
    "Internet das Coisas"
]

def buscar_informacoes(titulos):
    wiki_wiki = wikipediaapi.Wikipedia('pt', user_agent=USER_AGENT)
    for titulo in titulos:
        pagina = wiki_wiki.page(titulo)
        if pagina.exists():
            conteudo = pagina.text
            cursor.execute("INSERT INTO informacoes_wikipedia (titulo, conteudo) VALUES (?, ?)", (titulo, conteudo))
            print(f"Informações sobre '{titulo}' foram inseridas no banco de dados.")
        else:
            print(f"A página '{titulo}' não existe na Wikipédia.")

# Buscar informações e inserir no banco de dados
buscar_informacoes(titulos)

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados criado e informações inseridas com sucesso.")