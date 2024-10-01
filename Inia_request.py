import requests
import base64
import json

def resum_exame_execute(pdf_path):
    
    url = "https://main-inia-app.vercel.app/api/"
    
    # Ler e converter o PDF para base64
    try:
        with open(pdf_path, 'rb') as file:
            pdf_base64 = base64.b64encode(file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Arquivo {pdf_path} não encontrado.")
        return
    
    # Dados do paciente, pegue os inputs inseridos pelo usuário no site
    dados_paciente = {
        'data_de_nascimento': 'DD/MM/AAAA', 
        'Nome': 'NOME DO PACIENTE',
        'genero': 'masculino',#'feminino'
    }
    
    # Converter os dados do paciente para base64
    dados_paciente_bytes = json.dumps(dados_paciente).encode('utf-8')
    
    # Dados da requisição
    data = {
        'data': pdf_base64,
        'name': 'R831018_0405202417443122419750.pdf',
        'mime': 'application/pdf',
        'paciente': base64.b64encode(dados_paciente_bytes).decode('utf-8')
    }

    # Enviar a requisição POST
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Verifica se houve erro HTTP
        result = response.json()

        # Recuperar arquivos retornados
        normal_file_base64 = result.get('normal_file')
        anormal_file_base64 = result.get('anormal_file')
        diagnostic_file_base64 = result.get('diagnostic')
        

        # Salvar arquivos, se existirem
        if normal_file_base64:
            with open('files/normal_file.pdf', 'wb') as normal_file:
                normal_file.write(base64.b64decode(normal_file_base64))

        if anormal_file_base64:
            with open('files/anormal_file.pdf', 'wb') as anormal_file:
                anormal_file.write(base64.b64decode(anormal_file_base64))

        if diagnostic_file_base64:
            with open('files/diagnostic.docx', 'wb') as diagnostic_file:
                diagnostic_file.write(base64.b64decode(diagnostic_file_base64))

        print("Arquivos salvos com sucesso.")
    
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Erro na requisição: {req_err}")
    except ValueError:
        print("Erro: A resposta não é um JSON válido.")
        print(f"Conteúdo da resposta: {response.text}")


#So modifique essa parte
exame = r"C:\exemplo\SEUEXAME.pdf"                      #89.74

# Chamada da função
resum_exame_execute(exame) #Passe o path do arquivo pdf
