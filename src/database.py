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

    def salvar_vencedor(self, vencedor, nome):
        nome = nome.strip()

        self.cursor.execute("SELECT * FROM vencedores WHERE nome = ?", (nome,))
        resultado = self.cursor.fetchone()

        if resultado: 
            self.cursor.execute("UPDATE vencedores SET wins = wins + 1 WHERE nome = ?", (nome,))
        else:
            # Se o nome não existe, insere um novo registro
            self.cursor.execute("INSERT INTO vencedores (nome, wins) VALUES (?, ?)", (nome, 1))

        self.conn.commit()

    def select_nomes(self):
        # Selecionar e exibir todos os vencedores
        self.cursor.execute("select * from vencedores order by wins desc limit 10")
        vencedores = self.cursor.fetchall()

        return vencedores

    def fechar_conexao(self):
        # Fechar a conexão com o banco de dados
        self.conn.close()
