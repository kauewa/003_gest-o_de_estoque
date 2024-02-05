import sqlite3

# Conecte-se ao banco de dados SQLite (ou crie um se não existir)
conn = sqlite3.connect('dados.db')

# Crie um cursor
c = conn.cursor()

c.execute('''
    CREATE TABLE Produtos (
        COD TEXT UNIQUE,
        DATA_DE_CADASTRO TEXT,
        PRODUTO TEXT,
        MARCA TEXT,
        PESO_E_LÍQUIDO TEXT,
        UNIDADE_POR_FARDOS INTEGER,
        VALOR_POR_FARDO REAL
    )
''')

c.execute('''
    CREATE TABLE Compra (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        COD TEXT,
        DATA_DE_ENTRADA TEXT,
        FARDOS_INSERIDOS INTEGER,
        FOREIGN KEY(COD) REFERENCES Produtos(COD)
    )
''')

c.execute('''
    CREATE TABLE Venda (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        COD TEXT,
        DATA_DE_SAÍDA TEXT,
        FARDOS_VENDIDOS INTEGER,
        FOREIGN KEY(COD) REFERENCES Produtos(COD)
    )
''')


conn.commit()