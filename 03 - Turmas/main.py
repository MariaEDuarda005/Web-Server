# Navega no diretorio
import os
# Manipula e Cria um servidir (sem framework)
from http.server import SimpleHTTPRequestHandler
# Gerencia a comunicação com o cliente
import socketserver
from urllib.parse import urlparse, parse_qs
import hashlib
 
# Criação de Classe com artificio de HTTP
class MyMandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Tenta o Código abaixo
        try:
            # Tenta abrir o arquivo index.html
            f = open(os.path.join(path, 'index.html'), 'r')
            # Se existir, envia o conteudo do arquivo
            # Envia para o Cliente o Código de Sucesso
            self.send_response(200)
            # Forma de Tratmento
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # Leitura do HTML
            self.wfile.write(f.read().encode('utf-8'))
            # Finaliza para não contnuar o carregamento
            f.close
            return None
        # Caso dê erro
        except FileNotFoundError:
            pass
 
        return super().list_directory(path)
   
    def do_GET(self):
        if self.path =='/login':
            try:
                with open(os.path.join(os.getcwd(), 'login.html'), 'r') as login_file:
                    content = login_file.read()
                self.send_response(200)
                self.send_header("content-type","text/html")
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))          
        # Caso dê erro
            except FileNotFoundError:
                pass
            
        elif self.path == '/login_failed':
            # Responde ao cliente a mensagem de login/senha incorreta
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            
            # Lê o conteudo da pagina login.html
            with open(os.path.join(os.getcwd(), 'login.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
                
            # adiciona a mensagem de erro no conteudo da pagina
            mensagem = "Login e/ou senha incorreta. Tente novamente"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
            
            # Envia o conteudo modificado para o cliente
            self.wfile.write(content.encode('utf-8'))    
            
        elif self.path.startswith('/cadastro'):
            # Extraindo os parâmetros da URL

            query_params = parse_qs(urlparse(self.path).query)   
            login = query_params.get('login', [''])[0]
            senha = query_params.get('senha', [''])[0]

            # Mensagem de boas-vindas

            welcome_message = f"Olá {login}, seja bem-vindo! Percebemos que você é novo por aqui. Complete seu cadastro"

            # Responde ao cliente com a página de cadastro
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'confirmar_cadastro.html'), 'r', encoding='utf-8') as cadastro_file:

                content = cadastro_file.read()
                
            # substitue os marcadores pelos valores
            content = content.replace('{login}', login)
            content = content.replace('{senha}', senha)
            content = content.replace('{welcome_message}', welcome_message)
            
            # envia o conteudo modificado para o cliente
            self.wfile.write(content.encode('utf-8'))
            
            return # adicionando o return para evitar a execução do restante do codigo
        
        elif self.path.startswith('/tela_logada'):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'cadastro.html'), 'r', encoding='utf-8') as file:
                content = file.read()

                self.wfile.write(content.encode('utf-8'))
                
            
            # Obtem as turmas do arquivo e monta a tabela
            # turmas = self.obter_turmas()
            # tabela_turmas = ''
            # for turma in turmas:
            #     tabela_turmas += f'<tr><td>{turma["numero"]}</td><td>{turma["turma"]}</td><td>'
            #     tabela_turmas += '<div class="opcoes">'
            #     tabela_turmas += '<button class="adicionar">Adicionar</button>'
            #     tabela_turmas += '<button class="excluir">Excluir</button>'
            #     tabela_turmas += '</div></td></tr>'

            # # Substitui a marcação na página HTML pelos dados das turmas
            # content = content.replace('<!-- TURMAS_AQUI -->', tabela_turmas)

            # self.wfile.write(content.encode('utf-8'))
            return    
        
        elif self.path.startswith('/turmas'):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open(os.path.join(os.getcwd(), 'turmas.html'), 'r', encoding='utf-8') as file:
                content = file.read()
            self.wfile.write(content.encode('utf-8'))
            return
        
        # Ultima mudança - 23/02/2024 (16:32)
        elif self.path == '/turmas_failed':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers() 
            with open(os.path.join(os.getcwd(), 'turmas.html'), 'r', encoding='utf-8') as login_file:
                content = login_file.read()
            mensagem = "Turma ja existe em nosso banco"
            content = content.replace('<!-- Mensagem de erro será inserida aqui -->',
                                      f'<div class="error-message">{mensagem}</div>')
            self.wfile.write(content.encode('utf-8'))  

        else:
            super().do_GET()
            
    def usuario_existente(self, login, senha):
        if login == 'admin@gmail.com' and senha == 'senai':
            return login
                    
        return False
    
        #verifica se o login já existe
        # with open('dados.login.txt', 'r', encoding='utf-8') as file:
        #     for line in file:
        #         if line.strip():
        #             stored_login, stored_senha_hash, stored_name = line.strip().split(';')
        #         if login == stored_login:
        #             senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
        #             print(stored_senha_hash)
                    
        #             return senha_hash == stored_senha_hash
                    
        # return False
    
    def adicionar_usuario(self, login, senha, nome):
        senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()

        with open('dados.login.txt', 'a', encoding='UTF-8') as file:
            file.write(f'{login};{senha_hash};{nome}\n')  
            
    def adicionar_turmas(self, numero, turma):
        with open('dados.turmas.txt', 'a', encoding='utf-8') as files:
            files.write(f'{numero};{turma}\n')

            
    # def obter_turmas(self):
    #     turmas = []
    #     with open('dados.turmas.txt', 'r', encoding='utf-8') as file:
    #         for line in file:
    #             if line.strip():
    #                 numero, turma = line.strip().split(';')
    #                 turmas.append({'numero': numero, 'turma': turma})
    #     return turmas
 
    def do_POST(self):
        # Verifica se a rota é "/enviar_login"
        if self.path == '/enviar_login':
            # Obtém o comprimento do corpo da requesição
            content_length = int(self.headers['content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados o formulário
            form_data = parse_qs(body, keep_blank_values=True)
            
            login = form_data.get('email', [''])[0]
            senha = form_data.get('senha', [''])[0]
 
            print(form_data)
            # Exibe os dados no terminal
            print("DADOS DO FORMULÁRIO")
            print("E-mail:", login)
            print("Senha:", senha)
            
            
            if self.usuario_existente(login, senha):
                self.send_response(302)
                self.send_header('Location', '/tela_logada')
                self.end_headers()
                return
                                      
            else:
                if any(line.startswith(f"{login};") for line in open("dados.login.txt", "r", encoding="UTF-8")):
                    # redireciona para a pagina
                    self.send_response(302)
                    self.send_header('Location', '/login_failed')
                    self.end_headers()
                    return # adicionando um return para evitar a execução 
                
                else:
                    self.adicionar_usuario(login, senha, nome="None")
                    # with open ("dados_login.txt", "a", encoding="UTF-8") as file:
                    #     file.write(f"{login};{senha};" + "none" + "\n")
                    self.send_response(302)
                    self.send_header('Location', f'/cadastro?login={login}&senha={senha}')
                    self.end_headers()
                    
                    return # adicionando um return para evitar a execução 
                
        elif self.path.startswith('/confirmar_cadastro'):
                      
                # Obtém o comprimento do corpo da requisição
                content_length = int(self.headers['Content-Length'])
                # lê o corpo da requisição
                body = self.rfile.read(content_length).decode('utf-8')
                # parseia os dados dos formularios
                form_data = parse_qs(body, keep_blank_values=True)
                
                # query_params = parse_qs(urlparse(self.path).query)
                login = form_data.get('email', [''])[0]
                senha = form_data.get('senha', [''])[0]
                name = form_data.get('name', [''])[0]
                
                senha_hash = hashlib.sha256(senha.encode('UTF-8')).hexdigest()
                
                print("nome: " + name)

                if self.usuario_existente(login, senha):
                    
                    # with open(os.path.join(os.getcwd(), 'confirmar_cadastro.html'), 'r', encoding='utf-8') as file:
                    #     contentfile = file.read()
                        
                    # Atualiza o arquivo com o nome, se a senha estiver correta
                    with open('dados.login.txt', 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        
                    with open('dados.login.txt', 'w', encoding='utf-8') as file:
                        for line in lines:
                            stored_login, stored_senha, stored_name = line.strip().split(';')
                            
                            print(stored_login, stored_name, stored_senha)
                            
                            if login == stored_login and senha_hash == stored_senha:
                                line = f"{login};{senha_hash};{name}\n"
                                
                            file.write(line)
                    print("with usuário existente ")
                    
                    # redireciona o cliente para onde desejar após a confirmação
                    # self.send_response(302)
                    # self.send_header("Content-type", "text/html; charset=utf-8")
                    # self.end_headers()
                    # # self.wfile.write("Registro recebido com sucesso!!!".encode('utf-8'))
                    # self.wfile.write(contentfile.encode('utf-8'))
                    self.send_response(302)
                    self.send_header('Location', '/tela_logada')
                    self.end_headers()
                    
                # TEM MUITA CHANCE DE DAR ERRADO ESSA PARTE
                    
                if self.obter_turmas():
                    with open('dados.turmas.txt', 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        
                    with open('dados.login.txt', 'w', encoding='utf-8') as file:
                        for line in lines:
                            numero, turma = line.strip().split(';')                           
                            print(numero,turma)                                
                            file.write(lines)
                    
                    self.send_response(302)
                    self.send_header('Location', '/tela_logada')
                    self.end_headers()
                    
                else:
                    # se o usuario não existe ou a senha está incorreta, redirecione para outra pagina
                    #self.remover_ultima_linha('dados_login.txt')
                    self.send_response(302)
                    self.send_header("Content-type", "text/html; charset=utf-8")
                    self.end_headers()
                    self.wfile.write("A senha não confere. Retome o procedimento".encode('utf-8'))
                    
        elif self.path.startswith('/turmas'):
            # Obtém o comprimento do corpo da requisição
            content_length = int(self.headers['content-Length'])
            # Lê o corpo da requisição
            body = self.rfile.read(content_length).decode('utf-8')
            # Parseia os dados do formulário
            form_data = parse_qs(body, keep_blank_values=True)

            numero = form_data.get('numero', [''])[0]
            turma = form_data.get('turma', [''])[0]

            # Adiciona as turmas e obtém a lista atualizada
            turmas = self.adicionar_turmas(numero, turma)

            with open('dados.turmas.txt', 'r', encoding='utf-8') as file:
                lines = file.readlines()

            # self.send_response(302)
            # self.send_header('Location', '/tela_logada')
            # self.end_headers()
            
            # mudança para a senha - 23/02/2024 (16:32)
            if any(line.startswith(f"{numero};") for line in open("dados.turmas.txt", "r", encoding="UTF-8")):
                self.send_response(302)
                self.send_header('Location', '/turmas_failed')
                self.end_headers()
                return
           
            else:            
                self.adicionar_turmas(numero,turma)
                self.send_response(302)
                self.send_header("Content-type", "text/html; charset=utf-8")
                self.end_headers()
                    
        else:
            # Se não for a rota "/enviar_login", continua com o comportamento padrão
            super(MyMandler,self).do_POST()
            
 
 
# Define o IP  e a porta a serem utilizados
endereco_ip = "0.0.0.0"
porta = 8000
 
# Cria um servidor na porta e IP especificos
with socketserver.TCPServer((endereco_ip, porta), MyMandler) as httpd:
    print(f"Servidor iniciando em {endereco_ip}:{porta}")
    # Mantém o servidor em execução
    httpd.serve_forever()