import requests
import base64
import json
import os

url = "https://n8n.inia.app/webhook/"

endpoints = {
    'organization': {
        'login': 'organization/login',
        'signup':'organization/signup',
        'recovery-password': '' #EM BREVE
        },
'client': {
    'add':'organization/clients/add',
    'activate': 'organization/clients/activate',
    'list': 'organization/clients/list',
    'remove': '',  #EM BREVE
    'deactivate':'' #EM BREVE
},

'api': {
        'request': ''
    }

}


def requestOrganization(endpoint = '', payload = {}, token = None, method = 'POST'):    
    # Enviar a requisição POST
    try:
        if method =='POST':
            response = requests.post(url + endpoint, json=payload)
        else:
            response = requests.post(url + endpoint, json=payload)

        response.raise_for_status()  # Verifica se houve erro HTTP

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
        print(response.text) #Em muitos casos a causa do erro vem como resposta do webhook
    except requests.exceptions.RequestException as req_err:
        print(f"Erro na requisição: {req_err}")
    except ValueError:
        print("Erro: A resposta não é um JSON válido.")
        print(f"Conteúdo da resposta: {response.text}")


# Adicionado Usuário
def create_account(email, password):
    #Coloque a senha com no minimo 6 caracteres
    payload = {'auth': {'email': email, 'password': password}}
    endpoint = endpoints.get('organization').get('signup')
    response = requests.post(url + endpoint, json=payload)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    
    print(response.text)


def login(email, password):
    payload = {'auth': {'email': email , 'password': password}}
    endpoint = endpoints.get('organization').get('login')
    response = requests.post(url + endpoint, json=payload)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    
    return response.json().get('acess_token')

def add_user(client, acessToken):
    payload = {'client': {'username':client}}
    header = {'Authorization': f'Bearer {acessToken}'}
    endpoint = endpoints.get('client').get('add')
    response = requests.post(url + endpoint, json=payload, headers=header)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    print(response.text)

def activate_user(client, plan, acessToken):
    payload = {'client': {'username':client, 'plan': plan}}
    header = {'Authorization': f'Bearer {acessToken}'}
    endpoint = endpoints.get('client').get('activate')
    response = requests.post(url + endpoint, json=payload, headers=header)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    print(response.text)

def get_clients(acessToken):
    header = {'Authorization': f'Bearer {acessToken}'}
    endpoint = endpoints.get('client').get('list')
    response = requests.get(url + endpoint, headers=header)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    
    return response.json()

def api_call(client, acessToken, diretorio, pdf_path, paciente={}, output="df-pdf.df-pdf.docx.pdf", unknown=True):
    
    header = {'Authorization': f'Bearer {acessToken}'}
    
    url = "https://n8n.inia.app/webhook/organization/api"
    
    # Ler e converter o PDF para base64
    try:
        with open(pdf_path, 'rb') as file:
            pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Arquivo {pdf_path} não encontrado.")
        return
    
    # Converter os dados do paciente para base64
    dados_paciente_bytes = json.dumps(paciente).encode('utf-8')
    
    # Dados da requisição
    data = {
        'data': pdf_base64,
        'name': 'EXAME.pdf',
        'mime': 'application/pdf',
        'paciente': base64.b64encode(dados_paciente_bytes).decode('utf-8'),
        'output': output,
        'unknown': unknown
    }
    
    payload = {'client': {'username':client}, 'data': data}
    
    # Enviar a requisição POST
    try:
        response = requests.post(url, json=payload, headers=header)
        response.raise_for_status()  # Verifica se houve erro HTTP
        result = response.json()
        
        # Recuperar arquivos retornados
        normal_file_base64 = result.get('normal_file')
        anormal_file_base64 = result.get('anormal_file')
        diagnostic_file_base64 = result.get('diagnostic')
        
        if unknown:
            unknown_file_base64 = result.get('unknown')

        if diretorio:
            if not os.path.exists(diretorio):
                os.mkdir(diretorio)
        else:
            diretorio = ''
        
        # Salvar arquivos, se existirem
        if normal_file_base64:
            with open(f'{diretorio}/normal_file.pdf', 'wb') as normal_file:
                normal_file.write(base64.b64decode(normal_file_base64))

        if anormal_file_base64:
            with open(f'{diretorio}/anormal_file.pdf', 'wb') as anormal_file:
                anormal_file.write(base64.b64decode(anormal_file_base64))

        if diagnostic_file_base64:
            with open(f'{diretorio}/diagnostic.pdf', 'wb') as diagnostic_file:
                diagnostic_file.write(base64.b64decode(diagnostic_file_base64))
        
        if unknown_file_base64:
            if unknown_file_base64:
                with open(f'{diretorio}/unknown.pdf', 'wb') as unknown_file:
                    unknown_file.write(base64.b64decode(unknown_file_base64))
        

        print("Arquivos salvos com sucesso.")
        print(response.headers.items())
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erro na requisição: {req_err}")
    except ValueError:
        print("Erro: A resposta não é um JSON válido.")
        print(f"Conteúdo da resposta: {response.text}")

# variaveis
#diretorio do arquivo
diretorio = 'files'
exame = r"MEU-PDF.pdf"
output = "df-pdf.df-pdf.pdf.pdf" # df-pdf.df-pdf.docx.pdf

#Preencha os dados do paciente                
data_de_nascimento = 'DD/MM/AAAA'
genero = 'feminino' #masculino ou feminino

# Dados do paciente
dados_paciente = {
        'data_de_nascimento': data_de_nascimento, 
        'genero': genero, #'feminino' ou 'masculino'
    }

unknown = True

#Criar conta
create_account('myemail@gmail.com', 'password') #Nao esqueça de confirmar a inscricao no email
#login
acess_token = login('myemail@gmail.com', 'password')
#adiciona usuario
add_user('my_client', acessToken=acess_token) #Adiciona usuario

#ativa o usuario
activate_user('my-client', 'basic' , acess_token) # #basic, professional or enterprise

#lista usuarios
print(get_clients(acess_token))

# Chamada da API
api_call(client='inia-test-410', acessToken=acess_token, diretorio = diretorio, pdf_path = exame, paciente = dados_paciente, output= output, unknown = unknown) #Passe o path do arquivo pdf
