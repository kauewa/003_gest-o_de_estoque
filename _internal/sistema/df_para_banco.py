from src.db import Db
import pandas as pd

db = Db()


## Produtos
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
dados = pd.read_excel('Estoque.xlsx', sheet_name='Cadastro', header=6)
# Convertendo a coluna 'DATA DE CADASTRO' para o formato de string 'dd/mm/yyyy'
dados['DATA DE CADASTRO'] = dados['DATA DE CADASTRO'].dt.strftime('%d/%m/%Y')

# Renomeando as colunas para remover os espaços e substituir por '_'
dados.columns = [col.replace(' ', '_') for col in dados.columns]
dados.columns = [col.replace('(', '').replace(')', '') for col in dados.columns]
dados.rename(columns={'TOTAL_DE_SAÍDASFARDOS': 'TOTAL_DE_SAÍDAS_FARDOS'}, inplace=True)
dados = dados.drop(['ESTOQUE_ATUAL_POR_ITEM', 'VALOR_TOTAL', 'VALOR_UNITÁRIO', 'ESTOQUE_DE_FARDOS_INICIAL', 'INVESTIMENTO', 'TOTAL_DE_ENTRADAS_FARDOS', 'TOTAL_DE_SAÍDAS_FARDOS'], axis=1)

# Convertendo o DataFrame para um dicionário
dados_dict = dados.to_dict('records')
# # print(dados_dict)

for dado in dados_dict:
    # print(dado)
    db.insert('Produtos', dado)

result = db.select_all('Produtos')

print(result)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------

## Compras
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#COMPRAS INICIAIS
dados = pd.read_excel('Estoque.xlsx', sheet_name='Cadastro', header=6)
dados['DATA DE CADASTRO'] = dados['DATA DE CADASTRO'].dt.strftime('%d/%m/%Y')
dados.columns = [col.replace(' ', '_') for col in dados.columns]
dados.columns = [col.replace('(', '').replace(')', '') for col in dados.columns]
dados.rename(columns={'TOTAL_DE_SAÍDASFARDOS': 'TOTAL_DE_SAÍDAS_FARDOS', 'DATA_DE_CADASTRO': 'DATA_DE_ENTRADA', 'ESTOQUE_DE_FARDOS_INICIAL': 'FARDOS_INSERIDOS'}, inplace=True)
dados = dados.drop(['UNIDADE_POR_FARDOS','PRODUTO','MARCA','PESO_E_LÍQUIDO','VALOR_POR_FARDO','ESTOQUE_ATUAL_POR_ITEM', 'VALOR_TOTAL', 'VALOR_UNITÁRIO', 'INVESTIMENTO', 'TOTAL_DE_ENTRADAS_FARDOS', 'TOTAL_DE_SAÍDAS_FARDOS'], axis=1)
dados['COD'] = dados['COD'].astype(str)
# Convertendo o DataFrame para um dicionário
dados_dict = dados.to_dict('records')
# print(dados_dict)

for dado in dados_dict:
    # print(dado)
    db.insert('Compra', dado)

result = db.select_all('Compra')

print(result)

#OUTRAS COMPRAS

dados = pd.read_excel('Estoque.xlsx', sheet_name='Compra')
dados['COD'] = dados['COD'].astype(str)
dados['DATA DE ENTRADA'] = dados['DATA DE ENTRADA'].dt.strftime('%d/%m/%Y')
dados.columns = [col.replace(' ', '_') for col in dados.columns]
# print(dados.columns)
dados = dados.drop(['PRODUTO', 'MARCA', 'PESO_E_LÍQUIDO',
       'UNIDADE_POR_FARDOS', 'VALOR_POR_FARDO',
       'INVESTIMENTO_DE_ENTRADA_POR_PRODUTO'], axis=1)
dados['DATA_DE_ENTRADA'] = dados['DATA_DE_ENTRADA'].fillna('')

dados_dict = dados.to_dict('records')
print(dados_dict)

for dado in dados_dict:
    # print(dado)
    db.insert('Compra', dado)

result = db.select_all('Compra')

print(result)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------

## Vendas
#-----------------------------------------------------------------------------------------------------------------------------------------------------------
dados = pd.read_excel('Estoque.xlsx', sheet_name='Venda')
dados['COD'] = dados['COD'].astype(str)
dados['DATA DE SAÍDA'] = dados['DATA DE SAÍDA'].dt.strftime('%d/%m/%Y')
dados.columns = [col.replace(' ', '_') for col in dados.columns]
# print(dados.columns)

dados = dados.drop(['PRODUTO', 'MARCA', 'PESO_E_LÍQUIDO',
       'UNIDADE_POR_FARDOS', 'VALOR_POR_FARDOS',
       'VALOR_SAÍDA_POR_PRODUTO'], axis=1)

dados['DATA_DE_SAÍDA'] = dados['DATA_DE_SAÍDA'].fillna('')

dados_dict = dados.to_dict('records')
# print(dados_dict)

for dado in dados_dict:
    # print(dado)
    db.insert('Venda', dado)

result = db.select_all('Venda')

print(result)

