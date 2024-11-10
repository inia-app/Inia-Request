import requests
import base64
import json
import os

def resum_exame_execute(diretorio, pdf_path, paciente={}, output="pdf-3-docx-1"):
    
    url = "https://main-inia-app.vercel.app/api/"
    
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
        'output': output 
    }

    end_with = {"pdf-3-docx-1":['pdf','pdf','docx','pdf'], "csv-2-pdf-1-docx-1": ['csv','csv','docx','pdf']}

    # Enviar a requisição POST
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Verifica se houve erro HTTP
        result = response.json()

        # Recuperar arquivos retornados
        normal_file_base64 = result.get('normal_file')
        anormal_file_base64 = result.get('anormal_file')
        diagnostic_file_base64 = result.get('diagnostic')
        unknown_file_base64 = result.get('unknown')

        if diretorio:
            if not os.path.exists(diretorio):
                os.mkdir(diretorio)
        else:
            diretorio = ''
        # Salvar arquivos, se existirem
        if normal_file_base64:
            with open(f'{diretorio}/normal_file.{end_with[output][0]}', 'wb') as normal_file:
                normal_file.write(base64.b64decode(normal_file_base64))

        if anormal_file_base64:
            with open(f'{diretorio}/anormal_file.{end_with[output][1]}', 'wb') as anormal_file:
                anormal_file.write(base64.b64decode(anormal_file_base64))

        if diagnostic_file_base64:
            with open(f'{diretorio}/diagnostic.{end_with[output][2]}', 'wb') as diagnostic_file:
                diagnostic_file.write(base64.b64decode(diagnostic_file_base64))
        
        if unknown_file_base64:
            with open(f'{diretorio}/unknown.{end_with[output][3]}', 'wb') as unknown_file:
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


#diretorio do arquivo
diretorio = 'files'
exame = r"exams/SABIN4.pdf"
output = "pdf-3-docx-1" # csv-2-pdf-1-docx-1 | pdf-3-docx-1 (Mais detalhes no ReadME)

#Preencha os dados do paciente                
dados_paciente = {
        'data_de_nascimento': '18/08/1974', #dados de exemplo
        'genero': 'masculino', #'feminino' ou 'masculino'
    }

# Chamada da função
resum_exame_execute(diretorio = diretorio, pdf_path = exame, paciente = dados_paciente, output= output) #Passe o path do arquivo pdf