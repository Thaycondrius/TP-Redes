import socket
import threading

class Server(object):
    def __init__(self, port=8080):
        self.host = ''
        self.port = port
        self.content_dir = ''

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            print("Iniciando servidor no IP/Porta {host}:{port}".format(host=self.host, port=self.port))
            self.socket.bind((self.host, self.port))
            print("Servidor Iniciado.")

        except Exception as e:
            print("Erro ao iniciar servidor na porta: {port}".format(port=self.port))
            self.shutdown()
            sys.exit(1)
        self.listen()

    def header(self, code):
        header = ''
        if code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif code == 404:
            header += 'HTTP/1.1 404 Not Found\n'
        header += 'Connection: close\n\n'
        return header

    def listen(self):
        self.socket.listen(5)
        while True:
            (client, address) = self.socket.accept()
            print("Conectado pelo cliente: {addr}".format(addr=address))
            threading.Thread(target=self.clientc, args=(client, address)).start()

    def clientc(self, client, address):
        while True:
            req = client.recv(1024)
            if not req: break
            method = req.split(' ')[0]
            print("Metodo: {m}".format(m=method))
            print("Requisicao: {b}".format(b=req))

            if method == "GET":
                reqf = req.split(' ')[1]
                if reqf == "/":
                    reqf = "/index.html"
                remove = reqf.split('/')
                reqf = remove[1]
                fpath = self.content_dir + reqf
                print("Enviando pagina: [{fp}]".format(fp=fpath))
                try:
                    f = open(fpath, 'rb')
                    if method == "GET":
                        data = f.read()
                    f.close()
                    rheader = self.header(200)
                except Exception as e:
                    print("Arquivo nao encontrado. 404 enviado.")
                    rheader = self.header(404)
                    if method == "GET":
                        data = "404 Not Found"
                resp = rheader
                if method == "GET":
                    resp += data
                client.send(resp)
                client.close()
                break
            else:
                print("Metodo nao suportado: {method}, utilize o metodo GET.".format(method=method))

s = Server(8080)
s.start()
print("Ctrl+C para desligar o servidor.")
