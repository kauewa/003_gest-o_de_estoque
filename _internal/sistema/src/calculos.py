import pandas as pd
from src.db import Db

def select_produtos_home():
    db = Db()
    dados_produtos = db.select_all('Produtos')
    tabela = pd.DataFrame(dados_produtos)

    # Adicionando a coluna 'total de entradas(FARDOS)'
    tabela['total de entradas(FARDOS)'] = tabela.apply(lambda row: db.select_sum('Compra', 'FARDOS_INSERIDOS', {'COD': row['COD']}), axis=1)

    # Adicionando a coluna 'total de saídas(FARDOS)'
    tabela['total de saídas(FARDOS)'] = tabela.apply(lambda row: db.select_sum('Venda', 'FARDOS_VENDIDOS', {'COD': row['COD']}), axis=1)

    tabela = tabela.fillna(0)
    # Adicionando a coluna 'Estoque'
    tabela['Investimento'] = 'R$' + round(tabela['VALOR_POR_FARDO'] * tabela['total de entradas(FARDOS)'], 2).astype(str)

    tabela['Estoque'] = tabela['total de entradas(FARDOS)'] - tabela['total de saídas(FARDOS)']

    tabela['Valor total'] = 'R$' + round(tabela['VALOR_POR_FARDO'] * tabela['Estoque'], 2).astype(str)

    tabela['VALOR_POR_FARDO'] = 'R$' +  tabela['VALOR_POR_FARDO'].astype(str)

    tabela_html = tabela.to_html(index=False)
    db.__del__()
    return tabela_html


def select_vendas():
    db = Db()
    
    # Seleciona todos os dados das tabelas Vendas e Produtos
    dados_vendas = db.select_all('Venda')
    dados_produtos = db.select_all('Produtos')
    
    # Converte os dados para DataFrames do pandas
    tabela_vendas = pd.DataFrame(dados_vendas)
    tabela_produtos = pd.DataFrame(dados_produtos)
    
    # Renomeia a coluna 'COD' para permitir a fusão
    tabela_produtos = tabela_produtos.rename(columns={'COD': 'COD_PRODUTO'})
    
    # Combina as tabelas Vendas e Produtos
    tabela_vendas = pd.merge(tabela_vendas, tabela_produtos, how='left', left_on='COD', right_on='COD_PRODUTO')
    tabela_vendas = tabela_vendas.drop(columns=['ID'])

    tabela_vendas['VALOR SAÍDA'] = 'R$' + round(tabela_vendas['FARDOS_VENDIDOS'] * tabela_vendas['VALOR_POR_FARDO'],2).astype(str) 

    tabela_html = tabela_vendas.to_html(index=False)
    db.__del__()
    return tabela_html

def select_compras():
    db = Db()

    dados_compras = db.select_all('Compra')
    dados_produtos = db.select_all('Produtos')
    
    # Converte os dados para DataFrames do pandas
    tabela_compras = pd.DataFrame(dados_compras)
    tabela_produtos = pd.DataFrame(dados_produtos)
    
    # Renomeia a coluna 'COD' para permitir a fusão
    tabela_produtos = tabela_produtos.rename(columns={'COD': 'COD_PRODUTO'})
    
    # Combina as tabelas Vendas e Produtos
    tabela_compras = pd.merge(tabela_compras, tabela_produtos, how='left', left_on='COD', right_on='COD_PRODUTO')
    tabela_compras = tabela_compras.drop(columns=['ID'])

    tabela_compras['INVESTIMENTO'] = 'R$' + round(tabela_compras['FARDOS_INSERIDOS'] * tabela_compras['VALOR_POR_FARDO'],2).astype(str) 

    tabela_html = tabela_compras.to_html(index=False),
    db.__del__()
    return tabela_html


def select_soma_investimento():
    db = Db()

    dados_produtos = db.select_all('Produtos')
    tabela = pd.DataFrame(dados_produtos)

    # Adicionando a coluna 'total de entradas(FARDOS)'
    tabela['total de entradas(FARDOS)'] = tabela.apply(lambda row: db.select_sum('Compra', 'FARDOS_INSERIDOS', {'COD': row['COD']}), axis=1)
    tabela = tabela.fillna(0)
    # Adicionando a coluna 'Estoque'
    tabela['Investimento'] = tabela['VALOR_POR_FARDO'] * tabela['total de entradas(FARDOS)']

    investimento = tabela['Investimento'].sum()
    db.__del__()
    return investimento

def select_valor_atual():
    db = Db()
    dados_produtos = db.select_all('Produtos')
    tabela = pd.DataFrame(dados_produtos)

    # Adicionando a coluna 'total de entradas(FARDOS)'
    tabela['total de entradas(FARDOS)'] = tabela.apply(lambda row: db.select_sum('Compra', 'FARDOS_INSERIDOS', {'COD': row['COD']}), axis=1)

    # Adicionando a coluna 'total de saídas(FARDOS)'
    tabela['total de saídas(FARDOS)'] = tabela.apply(lambda row: db.select_sum('Venda', 'FARDOS_VENDIDOS', {'COD': row['COD']}), axis=1)

    tabela = tabela.fillna(0)
    # Adicionando a coluna 'Estoque'
    tabela['Investimento'] = 'R$' + round(tabela['VALOR_POR_FARDO'] * tabela['total de entradas(FARDOS)'], 2).astype(str)

    tabela['Estoque'] = tabela['total de entradas(FARDOS)'] - tabela['total de saídas(FARDOS)']

    tabela['Valor total'] = tabela['VALOR_POR_FARDO'] * tabela['Estoque']

    valor_atual = tabela['Valor total'].sum()
    db.__del__()
    return valor_atual

# def select_valor_venda():



