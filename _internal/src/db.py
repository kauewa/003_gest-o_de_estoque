import sqlite3



class Db:
    def __init__(self) -> None:
        self.banco = sqlite3.connect('dados.db')
        self.cursor = self.banco.cursor()

    def __del__(self):
        self.banco.close()

    def insert(self, tabela:str, dados:dict):
        # Convertendo os valores do dicionário para uma string
        colunas = ', '.join(dados.keys())
        valores = ', '.join([f"'{v}'" if isinstance(v, str) else str(v) for v in dados.values()])
        # print(colunas)
        # print(valores)
        query = f"""
        INSERT INTO {tabela} ({colunas}) VALUES ({valores})
        """

        print(query)
        self.cursor.execute(query)
        self.banco.commit()

    def update(self, tabela:str, cod:str, novos_dados:dict):
        # Convertendo os novos dados para o formato de uma instrução SQL UPDATE
        atualizacoes = ', '.join([f"{col} = '{val}'" if isinstance(val, str) else f"{col} = {val}" for col, val in novos_dados.items()])

        query = f"""
        UPDATE {tabela}
        SET {atualizacoes}
        WHERE COD = {cod}
        """
        self.cursor.execute(query)
        self.banco.commit()

    def select_all(self, tabela:str, colunas='*') -> list:
        try:
            query = f"""
            SELECT {colunas} from {tabela}
            """
            res = self.cursor.execute(query)
            
            # Obtendo os nomes das colunas
            nomes_das_colunas = [coluna[0] for coluna in res.description]

            # Obtendo todos os resultados
            resultados = res.fetchall()

            # Criando uma lista de dicionários
            lista_de_resultados = [dict(zip(nomes_das_colunas, resultado)) for resultado in resultados]

            return lista_de_resultados
        except:
            return []

    def select(self, tabela:str, where:dict):
        try:
            # Convertendo o dicionário 'where' em uma string de condições SQL
            condicoes = ' AND '.join([f"{chave} = '{valor}'" if isinstance(valor, str) else f"{chave} = {valor}" for chave, valor in where.items()])

            query = f"""
            SELECT * from {tabela} WHERE {condicoes}
            """
            res = self.cursor.execute(query)
            # Obtendo os nomes das colunas
            nomes_das_colunas = [coluna[0] for coluna in res.description]

            # Obtendo o resultado
            resultados = res.fetchall()

            # Criando uma lista de dicionários
            lista_de_resultados = [dict(zip(nomes_das_colunas, resultado)) for resultado in resultados]

            return lista_de_resultados
        except:
            return None
        
        
    def select_sum(self, tabela, coluna, where=None):
        if where is None:
            query = f"SELECT SUM({coluna}) FROM {tabela}"
        else:
            condicoes = ' AND '.join([f"{chave} = '{valor}'" if isinstance(valor, str) else f"{chave} = {valor}" for chave, valor in where.items()])
            query = f"SELECT SUM({coluna}) FROM {tabela} WHERE {condicoes}"
        self.cursor.execute(query)
        total = self.cursor.fetchone()[0]
        return total