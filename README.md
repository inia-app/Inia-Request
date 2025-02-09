# Inia V1.0.3

## Inia Auth

### Criando Conta
Crie uma conta fazendo uma requisição para o webhook:
```python
WEBHOOK_INSCRICAO = "https://n8n.inia.app/webhook/organization/signup" 
def create_account():
    
    #Coloque a senha com no minimo 6 caracteres
    payload = {'auth': {'email': 'your@email.com', 'password': 'password'}}
    response = requests.post(WEBHOOK_INSCRICAO, json=payload)
    
    try:
        response.raise_for_status()
    except:
        print(response.text)
    
    print(response.text)
```
### Login
Realize o login na conta para obter o token JWT com o acesso todos os recursos do INIA.
 - Para começar, tenha certeza de ter confirmado sua inscriçao pelo seu email. 
 - Caso ele tenha demorado a chegar, verifique se não está na caixa de spam.

```python
def login():
    payload = {'auth': {'email': 'nome@seuemail.com', 'password': 'minhasenha'}}
    endpoint = endpoints.get('organization').get('login')
    response = requests.post(url + endpoint, json=payload)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    
    return response.json().get('acess_token')

```


## Interagindo com API
Com o token de acesso, agora precisamos adicionar um cliente a conta que criamos.

### Adicionando Cliente
A organização não pode realizar requisições diretamente, mas sim através de clientes. Para cadastrar um usuário, basta definir um username e solicitar a adição. O username é um identificador único que permite encontrar com facilidade os dados sobre os seus clientes.


```python
def add_user(client, acessToken):
    payload = {'client': {'username':client}}
    header = {'Authorization': f'Bearer {acessToken}'}
    url = 'https://n8n.inia.app/webhook/organization/clients/add'
    response = requests.post(url, json=payload, headers=header)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    print(response.text) 
    
```

Se você recebeu um print escrito "user created", deu tudo certo. Se não, observe os logs, eles descrevem os erros mais comuns.

### Ativando Cliente
Com o cliente criado, ele precisa ser ativado para que possa interagir com a API.
Para ativar um cliente, é necessário que:
- O cliente pertença a sua organização.
- O username do cliente
- O plano do cliente:
    - basic: 200 requisições/mês
    - professional: 500 requisições/mês
    - enterprise: 1000 requisições/mês

```python
def activate_user(client, plan, acessToken):
    payload = {'client': {'username':client, 'plan': plan}}
    header = {'Authorization': f'Bearer {acessToken}'}
    url = "https://n8n.inia.app/webhook/organization/clients/activate"
    response = requests.post(url, json=payload, headers=header)
    try:
        response.raise_for_status()
    except:
        print(response.text)
    print(response.text)
```
### Chamando API para Análise de Exames

#### Disclaimers
- O arquivo enviado deve está em pdf
- DPI Recomendada: 300
- O arquivo enviado não possui defeitos que possam comprometer a leitura
- O INIA utiliza de algorítmos de visão compultacional, por isso é importante que o pdf esteja legível e na orientação devida para melhores resultados. Riscos ou falhas podem comprometer os resultados, assim como pdfs com textos ilegíveis ou embaçados.

#### Paramêtros
- diretorio: Pasta onde você deseja salvar os arquivos de saída do INIA, recomenda-se salvar em uma pasta para melhor organização.
- exame: Diretório em que o arquivo pdf está salvo.
- output: código de retorno, cada código está associado a tipos de retornos, segue o padrão:
    - df-pdf.df-pdf.docx.pdf: Retornos = anormal_file.pdf, normal_file.pdf, diagnostic.docx, unknown.pdf
    - df-pdf.df-pdf.pdf.pdf: Retornos = anormal_file.pdf, anormal_file.pdf, diagnostic.pdf, unknown.pdf
- paciente: Coloque os metadados dos pacientes, os dados podem influenciar no resultado final das análises, por isso é importante alimentar o campo com dados relevantes.

#### Codigo de Exemplo
```python
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
```


## Conclusão
- O INIA é uma excelente ferramenta para otimizar o atendimento ao paciente, contudo não substitui a responsabilidade médica na análise dos exames e/ou prescrição/diagnóstico do paciente.

*Em breve teremos uma grande atualização em nossos sistemas* INIA [2025]


