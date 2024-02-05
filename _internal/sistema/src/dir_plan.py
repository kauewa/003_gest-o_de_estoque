import os
import datetime

def organizar_arquivo(excel_file, nome):
    # Obtém a data atual
    agora = datetime.datetime.now()

    # Formata a data no formato desejado
    diamesano = agora.strftime('%d-%m-%Y')

    # Cria o nome do arquivo
    nome_arquivo = f"{nome}{diamesano}.xlsx"

    # Cria os diretórios de ano, mês e dia
    diretorio_ano = str(agora.year)
    meses = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
             7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
    diretorio_mes = meses[agora.month]
    diretorio_dia = str(agora.day)

    # Cria o caminho completo do diretório
    novo_diretorio = os.path.join('./Notas/', diretorio_ano, diretorio_mes, diretorio_dia)

    # Verifica se o diretório existe, se não, cria
    if not os.path.exists(novo_diretorio):
        os.makedirs(novo_diretorio)

    # Cria o caminho completo do novo arquivo
    novo_arquivo = os.path.join(novo_diretorio, nome_arquivo)

    # Salva o objeto BytesIO como um arquivo Excel no novo diretório
    with open(novo_arquivo, 'wb') as f:
        f.write(excel_file.read())

    # return nome_arquivo
