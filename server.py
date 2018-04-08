import socket
import sys
import threading

class WebServer(object):
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
        self._listen()

    def _generate_headers(self, response_code):
        header = ''
        if response_code == 200:
            header += 'HTTP/1.1 200 OK\n'
        elif response_code == 404:
            header += 'HTTP/1.1 404 Not Found\n'
        return header

    def _listen(self):
        self.socket.listen(5)
        while True:
            (client, address) = self.socket.accept()
            client.settimeout(60)
            print("Conectado pelo cliente: {addr}".format(addr=address))
            threading.Thread(target=self._handle_client, args=(client, address)).start()

    def _handle_client(self, client, address):
        while True:
            data = client.recv(1024).decode()
            if not data: break
            request_method = data.split(' ')[0]
            print("Metodo: {m}".format(m=request_method))
            print("Requisicao: {b}".format(b=data))

            if request_method == "GET":
                file_requested = data.split(' ')[1]
                if file_requested == "/":
                    file_requested = "index.html"
                filepath_to_serve = self.content_dir + file_requested
                print("Enviando pagina: [{fp}]".format(fp=filepath_to_serve))

                try:
                    f = open(filepath_to_serve, 'rb')
                    if request_method == "GET":
                        response_data = f.read()
                    f.close()
                    response_header = self._generate_headers(200)
                except Exception as e:
                    print("Arquivo nao encontrado. 404 enviado.")
                    response_header = self._generate_headers(404)
                    if request_method == "GET":
                        response_data = "404 Not Found"

                response = response_header.encode()
                if request_method == "GET":
                    response += response_data

                client.send(response)
                client.close()
                break
            else:
                print("Metodo nao suportado: {method}, utilize o metodo GET.".format(method=request_method))

server = WebServer(8080)
server.start()
print("Ctrl+C para desligar o servidor.")
