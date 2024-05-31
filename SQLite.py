import sqlite3

def conectar():
    conn = sqlite3.connect('perguntas_respostas.db')
    return conn

def criar_tabela(conn):
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS perguntas_respostas (
        pergunta TEXT,
        resposta TEXT
    )
    ''')
    conn.commit()

def inserir_pergunta_resposta(conn, pergunta, resposta):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO perguntas_respostas (pergunta, resposta) VALUES (?, ?)", (pergunta, resposta))
    conn.commit()

def listar_perguntas_respostas(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT pergunta, resposta FROM perguntas_respostas")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Pergunta: {row[0]}")
        print(f"Resposta: {row[1]}")
        print("------")

def buscar_resposta(conn, pergunta):
    cursor = conn.cursor()
    cursor.execute("SELECT resposta FROM perguntas_respostas WHERE pergunta = ?", (pergunta,))
    row = cursor.fetchone()
    if row:
        return row[0]
    else:
        return "Pergunta não encontrada."

def main():
    conn = conectar()
    criar_tabela(conn)

    while True:
        print("1. Inserir pergunta e resposta")
        print("2. Listar perguntas e respostas")
        print("3. Buscar resposta para uma pergunta")
        print("4. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            pergunta = input("Digite a pergunta: ")
            resposta = input("Digite a resposta: ")
            inserir_pergunta_resposta(conn, pergunta, resposta)
        elif opcao == '2':
            listar_perguntas_respostas(conn)
        elif opcao == '3':
            pergunta = input("Digite a pergunta a ser buscada: ")
            resposta = buscar_resposta(conn, pergunta)
            print(f"Resposta: {resposta}")
        elif opcao == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

    conn.close()

if __name__ == "__main__":
    main()