from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Carregar os dados
data = pd.read_csv('./dados/dados.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/info_descritivas')
def info_descritivas():
    # Obter informações descritivas dos dados
    num_rows = len(data)
    num_columns = len(data.columns)
    column_info = [{'name': col, 'type': str(data[col].dtype)} for col in data.columns]
    numeric_columns = data.select_dtypes(include=['number']).columns.tolist()
    stats = data[numeric_columns].describe()

    return render_template('descriptive_info.html', num_rows=num_rows, num_columns=num_columns, column_info=column_info, stats=stats)




@app.route('/filtrar', methods=['GET', 'POST'])
def filtrar():
    if request.method == 'POST':
        coluna = request.form.get('coluna')
        operador = request.form.get('operador')
        valor = request.form.get('valor')

        if coluna in data.columns:
            column_type = data[coluna].dtype
            if column_type == 'object':  # Coluna do tipo string
                resultado = data[data[coluna] == valor]
            elif column_type == 'int64' or column_type == 'float64':  # Coluna numérica
                valor = float(valor)
                if operador == 'igual':
                    resultado = data[data[coluna] == valor]
                elif operador == 'maior':
                    resultado = data[data[coluna] > valor]
                elif operador == 'menor':
                    resultado = data[data[coluna] < valor]
            else:
                resultado = pd.DataFrame(columns=data.columns)  # Criar um DataFrame vazio em caso de tipo desconhecido
        else:
            resultado = pd.DataFrame(columns=data.columns)  # Criar um DataFrame vazio em caso de coluna inexistente

        num_resultados = len(resultado)
        return render_template('filtro_resultado.html', num_resultados=num_resultados, resultado=resultado)

    return render_template('filtro.html', colunas=data.columns)







@app.route('/agrupar', methods=['GET', 'POST'])
def agrupar():
    if request.method == 'POST':
        coluna_agrupamento = request.form.get('coluna_agrupamento')
        funcao_agregacao = request.form.get('funcao_agregacao')

        if funcao_agregacao == 'max':
            resultado_agregado = data.groupby(coluna_agrupamento).max()
        elif funcao_agregacao == 'min':
            resultado_agregado = data.groupby(coluna_agrupamento).min()
        elif funcao_agregacao == 'mean':
            resultado_agregado = data.groupby(coluna_agrupamento).mean()
        elif funcao_agregacao == 'std':
            resultado_agregado = data.groupby(coluna_agrupamento).std()

        return render_template('agrupamento_resultado.html', coluna_agrupamento=coluna_agrupamento, funcao_agregacao=funcao_agregacao, resultado_agregado=resultado_agregado)

    return render_template('agrupamento.html', colunas=data.columns)


if __name__ == '__main__':
    app.run(debug=True)
