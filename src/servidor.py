import socket
import threading

# Configurações do Servidor
HOST = '127.0.0.1'  # Endereço local
PORT = 5000         # Porta para comunicação

# Lista para armazenar conexões dos clientes
clientes = []

def gerenciar_cliente(conn, addr):
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            # Recebe dados do cliente
            data = conn.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Recebido de {addr}: {data}")
            
            # Envia o dado para os outros clientes
            for cliente in clientes:
                if cliente != conn:
                    cliente.sendall(data.encode('utf-8'))
        except:
            break

    print(f"Cliente desconectado: {addr}")
    clientes.remove(conn)
    conn.close()

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(2)  # Limite de jogadores
    print(f"Servidor iniciado em {HOST}:{PORT}")
    
    while True:
        conn, addr = server.accept()
        clientes.append(conn)
        threading.Thread(target=gerenciar_cliente, args=(conn, addr)).start()

if __name__ == "__main__":
    iniciar_servidor()
