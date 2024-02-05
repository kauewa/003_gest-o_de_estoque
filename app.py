import os
import webview
import pandas as pd
from src.db import Db
from src.utils import dia_de_hoje, preencher_planilha_venda, float_para_dinheiro
from src.calculos import select_produtos_home, select_vendas, select_compras, select_soma_investimento, select_valor_atual
from flask import Flask, redirect, render_template, request, flash, Response, get_flashed_messages
from flask.helpers import make_response, send_file
from dotenv import load_dotenv
from src.dir_plan import organizar_arquivo


load_dotenv()
app = Flask(__name__, static_folder='./static', template_folder='./templates')
app.secret_key = os.getenv('SECRET_KEY')

webview.create_window('Gestão de estoque', app)

@app.route('/', methods=['GET'])
def init():
    return redirect('/home')

@app.route('/home', methods=['GET', 'POST'])
def home():
    valor_em_estoque = select_valor_atual()
    investimento = select_soma_investimento()
    valor_vendido = investimento - valor_em_estoque
    tabela_html = select_produtos_home()
    return render_template(
        'home.html', 
        tabela=tabela_html, 
        investimento=float_para_dinheiro(investimento) , 
        valor_em_estoque=float_para_dinheiro(valor_em_estoque),
        valor_vendido=float_para_dinheiro(valor_vendido)
        )

@app.route('/compras', methods=['GET', 'POST'])
def compras():
    tabela_html = select_compras()

    return render_template('compras.html', tabela=tabela_html)

@app.route('/vendas', methods=['GET', 'POST'])
def vendas():
    tabela_html = select_vendas()

    return render_template('vendas.html', tabela=tabela_html)

@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
    
    if request.method == 'POST':
        db = Db()
        cod = request.form.get('COD')
        produto = request.form.get('PRODUTO')
        marca = request.form.get('MARCA')
        peso_liquido = request.form.get('PESO_E_LÍQUIDO')
        unidade_peso_liquido = request.form.get('unidade_medida')
        peso_liquido = peso_liquido + unidade_peso_liquido
        unidade_por_fardos = request.form.get('UNIDADE_POR_FARDOS')
        valor_por_fardo = request.form.get('VALOR_POR_FARDO')

        existe_cod = db.select('Produtos', {'COD': cod})   
        existe_produto = db.select('Produto', {
            'PRODUTO': produto,
            'MARCA': marca,
            'PESO_E_LÍQUIDO': peso_liquido,
            'UNIDADE_POR_FARDOS': unidade_por_fardos,
        })
      
        if existe_cod:
            flash(f'Ja existe o COD {cod}', 'error')
        elif existe_produto:
            flash(f'Ja existe o produto {produto}, {marca}, {peso_liquido}, quantidade por fardo: {unidade_por_fardos}', 'error')
        else:
            try:
                db.insert('Produtos', {
                    'COD': cod,
                    'DATA_DE_CADASTRO': dia_de_hoje(),
                    'PRODUTO': produto,
                    'MARCA': marca,
                    'PESO_E_LÍQUIDO': peso_liquido,
                    'UNIDADE_POR_FARDOS': int(unidade_por_fardos),
                    'VALOR_POR_FARDO': float(valor_por_fardo)
                })
                flash('Cadastro realizado com sucesso!')
            except Exception as e:
                flash(f'Erro de banco - ERRO: {e}')
        
        db.__del__()


    return render_template('cadastro_produto.html')

@app.route('/cadastro_venda', methods=['GET', 'POST'])
def cadastro_venda():
    db = Db()
    produtos = db.select_all('Produtos')
    db.__del__()

    if request.method == 'POST':
        db = Db()
        nome = request.form.get('nome')
        cods = request.form.getlist('COD[]')
        fardos = request.form.getlist('FARDOS[]')
        dados = []
        try:
            for cod, fardo in zip(cods, fardos):
            
                produto = db.select('Produtos', {'COD': cod})
                db.insert('Venda', {
                    'COD': str(cod),
                    'DATA_DE_SAÍDA': dia_de_hoje(),
                    'FARDOS_VENDIDOS': fardo
                })
                venda = {
                    'COD_P': cod,
                    'PRODUTO': produto[0]['PRODUTO'],
                    'PESO E LÍQUIDO': produto[0]['PESO_E_LÍQUIDO'],
                    'FARDOS': fardo,
                    'UNIDADE POR FARDOS': produto[0]['UNIDADE_POR_FARDOS'],
                    'VALOR UNITARIO': produto[0]['VALOR_POR_FARDO'] / float(produto[0]['UNIDADE_POR_FARDOS']),
                    'VALOR POR FARDO': produto[0]['VALOR_POR_FARDO']
                }
                dados.append(venda)
        except Exception as e:
            flash(f'Erro ao cadastrar venda do produto {cod} - ERRO: {e}')
            produto = db.select('Produtos', {'COD': cod})


        flash('Venda cadastrada')
        db.__del__()
        excel_file = preencher_planilha_venda(dados, nome)
        organizar_arquivo(excel_file, nome)
        # response = make_response(send_file(excel_file, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', as_attachment=True, download_name=nome_arquivo))

        # return response

    return render_template('cadastro_venda.html', produtos=produtos)

@app.route('/cadastro_compra', methods=['GET', 'POST'])
def cadastro_compra():
    db = Db()
    produtos = db.select_all('Produtos')
    db.__del__()

    if request.method == 'POST':
        db = Db()
        cods = request.form.getlist('COD[]')
        fardos = request.form.getlist('FARDOS[]')

        try:
            for cod, fardo in zip(cods, fardos):
                db.insert('Compra', {
                    'COD': str(cod),
                    'DATA_DE_ENTRADA': dia_de_hoje(),
                    'FARDOS_INSERIDOS': fardo
                })
            flash('Compra cadastrada')
        except Exception as e:
            flash(f'Erro ao cadastrar venda do produto {cod} - ERRO: {e}' )


    return render_template('cadastro_compra.html', produtos=produtos)





if __name__ == '__main__':
    webview.start()

