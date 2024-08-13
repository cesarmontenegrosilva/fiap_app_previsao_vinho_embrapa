import requests
import pandas as pd
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, render_template
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Configurar matplotlib para usar o backend Agg
import matplotlib
matplotlib.use('Agg')

# URLs que você deseja acessar
URLS = {
    'producao': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02',
    'processamento': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03',
    'comercializacao': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04',
    'importacao': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05',
    'exportacao': 'http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06',
}

# Headers para simular um navegador (opcional)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# Função para coletar dados de uma categoria específica
def coletar_dados(url):
    dados_categoria = []
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), "html.parser")
        subcategorias = soup.find_all("button", class_="btn_sopt")
        
        if not subcategorias:
            for ano in range(1970, 2024):
                params = {"ano": ano}
                response_ano = requests.get(url, headers=headers, params=params)
                response_ano.encoding = 'utf-8'

                if response_ano.status_code == 200:
                    soup_ano = BeautifulSoup(response_ano.content.decode('utf-8', 'ignore'), "html.parser")
                    tabela = soup_ano.find("table", {"class": "tb_base tb_dados"})

                    if tabela:
                        linhas = tabela.find_all("tr")
                        for linha in linhas:
                            colunas = linha.find_all("td")
                            dados_linha = [coluna.text.strip() for coluna in colunas]
                            dados_categoria.append({"ano": ano, "dados": dados_linha})
        
        for subcategoria in subcategorias:
            subopcao = subcategoria['value']
            titulo_subcategoria = subcategoria.text.strip()
            
            for ano in range(1970, 2024):
                params = {"ano": ano, "subopcao": subopcao}
                response_ano = requests.get(url, headers=headers, params=params)
                response_ano.encoding = 'utf-8'

                if response_ano.status_code == 200:
                    soup_ano = BeautifulSoup(response_ano.content.decode('utf-8', 'ignore'), "html.parser")
                    tabela = soup_ano.find("table", {"class": "tb_base tb_dados"})
                    
                    if tabela:
                        linhas = tabela.find_all("tr")
                        for linha in linhas:
                            colunas = linha.find_all("td")
                            dados_linha = [coluna.text.strip() for coluna in colunas]
                            dados_categoria.append({"subcategoria": titulo_subcategoria, "ano": ano, "dados": dados_linha})
    
    return dados_categoria

# Função para preparar os dados de comercialização para o Prophet
def preparar_dados(data):
    vendas_vinho_fino_tinto = []
    anos = []

    for i in range(len(data)):
        ano = data[i]['ano']
        dados = data[i]['dados']
        
        if 1970 <= ano <= 2023:
            if len(dados) > 0 and dados[0] == "VINHO FINO DE MESA":
                if i + 1 < len(data) and len(data[i + 1]['dados']) > 0 and data[i + 1]['dados'][0] == "Tinto":
                    venda = data[i + 1]['dados'][1]
                    vendas_vinho_fino_tinto.append(venda)
                    anos.append(ano)

    df_final = pd.DataFrame({
        'ano': anos,
        'venda_vinho_fino_tinto': vendas_vinho_fino_tinto
    })

    if not df_final.empty:
        df_final['venda_vinho_fino_tinto'] = df_final['venda_vinho_fino_tinto'].str.replace('.', '').astype(float)

    return df_final

# Função para treinar o modelo Prophet
def treinar_modelo(df):
    model = Prophet()
    model.fit(df)
    return model

# Função para prever com o modelo Prophet
def prever_comercializacao(model, num_periodos):
    future = model.make_future_dataframe(periods=num_periodos, freq='YE')
    forecast = model.predict(future)
    return forecast

# Função para avaliação do modelo
def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def avaliar_modelo(df, forecast):
    y_true = df['y']
    y_pred = forecast['yhat'][:len(y_true)]
    
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_true, y_pred)
    mape = mean_absolute_percentage_error(y_true, y_pred)
    
    return mae, rmse, r2, mape

# Função para plotar o gráfico
def plotar_grafico(df, forecast, num_periodos):
    plt.figure(figsize=(20, 16))
    plt.plot(df['ds'], df['y'], label='Histórico', color='blue')
    plt.plot(forecast['ds'], forecast['yhat'], label='Previsão', color='orange')
    plt.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'], color='orange', alpha=0.2)
    ultimo_ano_historico = df['ds'].max()
    plt.axvline(x=ultimo_ano_historico, color='red', linestyle='--', label='Início da Previsão')
    plt.xlim(df['ds'].min(), forecast['ds'].max())

    for i in range(num_periodos):
        ano_previsto = forecast['ds'].iloc[-(num_periodos - i)].year
        yhat_previsto = forecast['yhat'].iloc[-(num_periodos - i)]
        plt.text(forecast['ds'].iloc[-(num_periodos - i)], yhat_previsto, str(ano_previsto), 
                 horizontalalignment='center', verticalalignment='bottom', fontsize=10, color='orange')

    plt.xlabel('Ano', fontsize=20)
    plt.ylabel('Comercialização (Vinho Fino de Mesa Tinto)', fontsize=20)
    plt.title('Previsão de Comercialização com Prophet', fontsize=20)
    plt.legend(fontsize=20)
    plt.grid(True)

    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return image_base64

# Inicializar a aplicação Flask
app = Flask(__name__)

# Página inicial para previsão
@app.route('/', methods=['GET', 'POST'])
def previsao():
    if request.method == 'POST':
        num_periodos = int(request.form['periodos'])

        # Coletar e preparar os dados de comercialização
        data = coletar_dados(URLS['comercializacao'])
        dados = preparar_dados(data)

        df = pd.DataFrame({
            'ds': pd.to_datetime(dados['ano'], format='%Y', errors='coerce'),
            'y': dados['venda_vinho_fino_tinto']
        })

        # Treinar o modelo e fazer a previsão
        modelo = treinar_modelo(df)
        previsao_df = prever_comercializacao(modelo, num_periodos)
        avaliacao = avaliar_modelo(df, previsao_df)
        grafico_base64 = plotar_grafico(df, previsao_df, num_periodos)

        # Formatar as previsões
        previsoes_formatadas = []
        for previsao_item in previsao_df[['ds', 'yhat']].tail(num_periodos).to_dict(orient='records'):
            previsao_formatada = {
                'ds': previsao_item['ds'],
                'yhat': "{:,.2f}".format(previsao_item['yhat'])
            }
            previsoes_formatadas.append(previsao_formatada)

        # Resultados formatados
        resultados = {
            "mae": "{:,.2f}".format(avaliacao[0]),
            "rmse": "{:,.2f}".format(avaliacao[1]),
            "r2": "{:,.2f}".format(avaliacao[2]),
            "mape": "{:,.2f}".format(avaliacao[3]),
            "previsoes": previsoes_formatadas,
            "grafico": grafico_base64
        }

        return render_template('previsao.html', resultados=resultados)

    return render_template('previsao.html')

# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)