import socket

HOST = '127.0.0.1'
PORT = 5000

def cliente():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"Conectado ao servidor em {HOST}:{PORT}")
    
    while True:
        try:
            # Envia mensagem ao servidor
            msg = input("Digite sua mensagem: ")
            if msg.lower() == 'sair':
                print("Encerrando conexão...")
                break
            client.send(msg.encode('utf-8'))

            # Recebe mensagens do servidor
            resposta = client.recv(1024).decode('utf-8')
            print(f"Mensagem recebida: {resposta}")
        except:
            print("Erro na conexão.")
            break
    
    client.close()

if __name__ == "__main__":
    cliente()
