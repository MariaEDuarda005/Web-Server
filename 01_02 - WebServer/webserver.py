import os
from http.server import SimpleHTTPRequestHandler
import socketserver

# socket - gerenciamento de acessos paa o sistema (servidor), gerencia a comunicação cliente servidor

class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            #tenta abrir um arquivo index.html
            f = open(os.path.join(path, 'pagina2.html'), 'r')
            #se existir, envia os o conteudo do arquivo
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
            # finalizar sem ter que ficar carregando na pagina do usuario
            f.close()
            return None
        except FileNotFoundError:
            pass
        
        return super().list_directory(path)
    
    
#Define um endereço de ip e a porta que foi utilizado
endereco_ip = "0.0.0.0"
porta = 8000

#Cria um servidor na porta e IP especificados
with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciado em {endereco_ip}:{porta}")
    # forever - ficar escutando para sempre
    httpd.serve_forever()
    