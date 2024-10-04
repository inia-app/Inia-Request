# INIA REQUEST V 1.0.1

## Autorização
- O INIA permite chamadas não autenticadas de qualquer dispositivo.

## Chamada
- Como entrada, envie o diretorio do arquivo para função resum_exam-execute()
- Altere apenas as variáveis:
  - paciente = NOME DO PACIENTE (opcional)
  - data_de_nascimento = DATA DE NASCIMENTO DO PACIENTE COM O PADRÃO = "DD/MM/AAAA"
  - genero = GENERO DO SEU PACIENTE ("masculino" ou "feminino")

## Retorno
- Adicione o diretório desejado dentro da variável diretorio, ex: diretorio = "files"
- As tabelas são salvas em pdf, e o diagnóstico em docx.
