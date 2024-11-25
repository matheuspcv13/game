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
    clientes.append(conn)  # Adiciona o cliente à lista de conexões

    # Envia uma mensagem inicial para o cliente que se conectou
    conn.sendall("Aguardando o outro jogador...".encode('utf-8'))

    while True:
        try:
            data = conn.recv(1024)  # Recebe dados do cliente
            if not data:
                break  # Se a conexão for fechada, sai do loop

            print(f"Recebido de {addr}: {data}")

            # Envia a mensagem recebida para todos os outros clientes
            for cliente in clientes:
                if cliente != conn:
                    cliente.sendall(data)  # Envia os dados para todos, exceto o remetente

            # Se for o primeiro cliente a enviar a mensagem (por exemplo, jogador 1),
            # o servidor pode enviar dados adicionais ou sinais para sincronizar a visão.
            for cliente in clientes:
                if cliente != conn:
                    cliente.sendall(data)

        except:
            break  # Se houver um erro, sai do loop

    # Quando o cliente desconecta
    print(f"Cliente desconectado: {addr}")
    clientes.remove(conn)  # Remove o cliente da lista
    conn.close()  # Fe

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
