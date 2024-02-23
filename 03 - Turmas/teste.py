import os
import hashlib
import socketserver
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
 
# Classe HTTP
class MyHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        try:
            # Abre o arquivo index.html
            f = open(os.path.join(path, 'index.html'), 'r')
 
            # Código de resposta para o cliente
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read().encode('utf-8'))
 
            f.close()
 
            return None
       
        except FileNotFoundError:
            print("hahahha")
 
        return super().list_directory(path)
   
    def do_GET(self):
 
        # Rota login
        if self.path == '/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
 
                self.send_response(200)
                self.send_header("content-type", "text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
 
            except FileNotFoundError:
                print("Hhahaahahhahhahahhahahhahaahahahhahaa")
 
        elif self.path == '/login_failed':
 
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               
            # adiciona a mensagem de erro no conteudo da pagina
            mensagem = "Login e/ou senha incorreta. Tente novamente"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
           
            # Envia o conteudo modificado para o cliente
            self.wfile.write(content.encode('utf-8'))
 
        elif self.path.startswith('/tela_professor'):
            print("entrou tela professor")
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as file:
                content = file.read()
 
                self.wfile.write(content.encode('utf-8'))
           
            return
       
        elif self.path.startswith('/tela_turma'):
            self.send_response(200)
            self.send_header("content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            with open(os.path.join(os.getcwd(), 'turmas.html'), 'r', encoding='utf-8') as file:
                content = file.read()
 
                self.wfile.write(content.encode('utf-8'))
           
            return
       
        elif self.path == '/cadastro_failed':
 
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
 
            with open(os.path.join(os.getcwd(), 'turmas.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
               
            print("algo deu errado")
           
            # Envia o conteudo modificado para o cliente
            self.wfile.write(content.encode('utf-8'))
       
        else:
            super().do_GET()
 
    def usuario_existente(self, login, senha):
        if login == 'admin' and senha == 'admin@senai':
            return login
       
        return False
 
    def adicionar_usuario(self, nome, professor):
        with open('dados.turma.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{nome};{professor}\n')  
   
    def do_POST(self):
       
        if self.path == '/enviar_login':
            content_length = int(self.headers['content-length'])
 
            body = self.rfile.read(content_length).decode('utf-8')
 
            form_data = parse_qs(body, keep_blank_values=True)
 
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]
 
            # Dados do formulario
 
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", login)
            print("Senha:", senha)
 
            # Verificando se o usuário já existe
 
            if self.usuario_existente(login, senha):
                print("tela_professor")
                self.send_response(302)
                print("tela_professor 2")
                self.send_header('Location', '/tela_professor')
                self.end_headers()
 
                return
           
            else:
                print("login_failed")
                self.send_response(302)
                self.send_header('Location', '/login_failed')
                self.end_headers()
                return  
           
        elif self.path.startswith('/cadastrar_turma'):
            content_length = int(self.headers['content-length'])
 
            body = self.rfile.read(content_length).decode('utf-8')
 
            form_data = parse_qs(body, keep_blank_values = True)
 
            nome_turma = form_data.get('nome-turma', [''])[0]
            professor = form_data.get('professor', [''])[0]
 
            if nome_turma.strip() == '' or professor.strip() == '':
                # Se algum campo estiver vazio, redireciona para a página de cadastro falhado
                self.send_response(302)
                self.send_header("Location", "/cadastro_failed")
                self.end_headers()
                return
            else:
                # Se os campos estiverem preenchidos, adiciona a turma
                self.adicionar_usuario(nome_turma, professor)
 
                self.send_response(302)
                self.send_header("Location", "/tela_professor")
                self.end_headers()
           
        else:
            super(MyHandler,self).do_POST()
 
       
 
endereco_ip = "0.0.0.0"
porta = 8000
 
# Cria um servidor na porta e IP especificos
with socketserver.TCPServer((endereco_ip, porta), MyHandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    # Mantém o servidor em execução
    httpd.serve_forever()
           