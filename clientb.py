import socket
HOST = ''
PORT = 8080
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print("Conectado ao servidor. IP:{host}:{port}".format(host=HOST, port=PORT))
print 'Para sair use CTRL+C\n'
msg = raw_input("url :")
tcp.send ("GET /"+msg)
resposta = tcp.recv(200096)
conteudo = resposta.split('\n\n', 1)
arquivo = conteudo[1]
print arquivo
if arquivo != "404 Not Found":
    arqr = open(msg, "wb")
    arqr.write(arquivo)
    arqr.close()
tcp.close()
