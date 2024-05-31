import sqlite3

# Conectar ao banco de dados (ou criar, se não existir)
conn = sqlite3.connect('perguntas_respostas.db')
cursor = conn.cursor()

# Criar a tabela perguntas_respostas, se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS perguntas_respostas (
    pergunta TEXT,
    resposta TEXT
)
''')

# Inserir informações sobre Marte
informacoes_sobre_marte = [
    ("Qual é a distância de Marte ao Sol?", "A distância média de Marte ao Sol é de cerca de 228 milhões de quilômetros."),
    ("Qual é a duração de um dia em Marte?", "Um dia em Marte, também conhecido como 'sol', tem cerca de 24 horas e 39 minutos."),
    ("Qual é a duração de um ano em Marte?", "Um ano em Marte dura cerca de 687 dias terrestres."),
    ("Marte tem satélites naturais?", "Sim, Marte tem dois satélites naturais: Fobos e Deimos."),
    ("Qual é a composição da atmosfera de Marte?", "A atmosfera de Marte é composta principalmente por dióxido de carbono (cerca de 95%), com traços de nitrogênio e argônio."),
    ("Existe água em Marte?", "Sim, há evidências de água em forma de gelo nos polos e de água líquida em salmouras na superfície."),
    ("Marte já foi visitado por missões espaciais?", "Sim, Marte foi visitado por várias missões espaciais, incluindo sondas orbitais, landers e rovers."),
    ("Qual é a temperatura média em Marte?", "A temperatura média em Marte é de cerca de -63°C, mas pode variar de cerca de -140°C a 30°C."),
    ("Marte tem vulcões?", "Sim, Marte tem vulcões, incluindo Olympus Mons, o maior vulcão do Sistema Solar."),
    ("Marte tem estações do ano?", "Sim, Marte tem estações do ano devido à inclinação de seu eixo, semelhante à Terra.")
]

# Inserir informações no banco de dados
cursor.executemany("INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (?, ?)", informacoes_sobre_marte)

# Salvar as alterações e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados criado e informações sobre Marte inseridas com sucesso.")