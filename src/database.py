import sqlite3

class Database:
    def __init__(self, db_name='vencedores.db'):
        # Conectar ao banco de dados e criar o cursor
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Criar a tabela se não existir
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS vencedores (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            wins INTEGER NOT NULL
        )
        ''')
        self.conn.commit()

    def salvar_vencedor(self, nome):
        self.cursor.execute("INSERT INTO vencedores (nome, wins) VALUES (?, 1)", (nome,))
        self.conn.commit()
        
        self.cursor.execute("SELECT nome FROM vencedores WHERE nome = ?", (nome,))
        novo_jogador = self.cursor.fetchall()
        
        
        print(novo_jogador)


    def select_nomes(self):
        self.cursor.execute("SELECT * FROM vencedores")
        vencedores = self.cursor.fetchall()

        # Exibir resultados no console
        for vencedor in vencedores:
            print(f"ID: {vencedor[0]}, Nome: {vencedor[1]}")

    def fechar_conexao(self):
        self.conn.close()
