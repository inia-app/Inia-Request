# Inia V1.0.2

## Requisitando o INIA

### Certifique-se
- O arquivo enviado está em pdf
- DPI Recomendada: 300
- O arquivo enviado não possui defeitos que possam comprometer a leitura
- O INIA utiliza de algorítmos de visão compultacional, por isso é importante que o pdf esteja legível e na orientação devida para melhores resultados. Riscos ou falhas podem comprometer os resultados, assim como pdfs com textos ilegíveis ou embaçados.

### Paramêtros
- diretorio: Pasta onde você deseja salvar os arquivos de saída do INIA, recomenda-se salvar em uma pasta para melhor organização.
- exame: Diretório em que o arquivo pdf está salvo.
- output: código de retorno, cada código está associado a tipos de retornos, segue o padrão:
    - pdf-3-docx-1(default): Retornos = anormal_file.pdf, normal_file.pdf, diagnostic.docx, unknown.pdf
    - csv-2-pdf-1-docx-1: Retornos = anormal_file.csv, anormal_file.csv, diagnostic.docx, unknown.pdf
- paciente: Coloque os metadados dos pacientes, os dados podem influenciar no resultado final das análises, por isso é importante alimentar o campo com dados relevantes.

## Conclusões e Avisos
- O INIA é uma excelente ferramenta para otimizar o atendimento ao paciente, contudo não substitui a responsabilidade médica na análise dos exames e/ou prescrição/diagnóstico do paciente.