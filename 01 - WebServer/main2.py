from http.server import SimpleHTTPRequestHandler, HTTPServer

#Defina a porta em que o servidor vai escutar
port = 8000

#Defina o manipulador de requisições
handler = SimpleHTTPRequestHandler

#Crie uma instancia do servidor
server = HTTPServer(('localhost', port), handler)

#Imprima uma mensagem indicando que o servidor está rodando
print(f"O servidor rodando em http://localhost:{port}")

#Inicie o servidor
server.serve_forever()