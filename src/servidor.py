import socket
import threading
from jogo import jogo  # Importa o jogo local
from database import Database

HOST = '127.0.0.1'
PORT = 5000

# Lista para armazenar as conexões dos jogadores
clientes = []

def gerenciar_cliente(conn, addr, server):
    print(f"Cliente conectado: {addr}")
    # Enviar uma mensagem de boas-vindas
    conn.sendall("Aguardando o outro jogador...".encode('utf-8'))

    # Adiciona o cliente à lista de jogadores
    clientes.append(conn)

    # Esperar até que dois jogadores estejam conectados
    if len(clientes) == 1:
        for cliente in clientes:
            cliente.sendall("Ambos os jogadores estão conectados! O jogo pode começar.".encode('utf-8'))

    while True:
        try:
            # Recebe dados do jogador
            data = conn.recv(1024)
            if not data:
                break
            print(f"Recebido de {addr}: {data}")

            # O servidor envia o estado do jogo para os outros jogadores
            for cliente in clientes:
                if cliente != conn:
                    cliente.sendall(data)

        except:
            break

    print(f"Cliente desconectado: {addr}")
    clientes.remove(conn)
    conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(3)  # Aceita até 2 jogadores
    print(f"Servidor iniciado em {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=gerenciar_cliente, args=(conn, addr, server)).start() 


if __name__ == "__main__":
    iniciar_servidor()
