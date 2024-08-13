import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify

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
    
    # Primeiro, precisamos encontrar todas as subcategorias disponíveis na página
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Definir o encoding como UTF-8

    if response.status_code == 200:
        soup = BeautifulSoup(response.content.decode('utf-8', 'ignore'), "html.parser")
        
        # Encontrar os botões que correspondem às subcategorias
        subcategorias = soup.find_all("button", class_="btn_sopt")
        
        # Se não houver subcategorias, coletar os dados diretamente
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
                            dados_categoria.append({
                                "ano": ano,
                                "dados": dados_linha
                            })
        
        # Caso haja subcategorias, coletar os dados para cada uma delas
        for subcategoria in subcategorias:
            subopcao = subcategoria['value']
            titulo_subcategoria = subcategoria.text.strip()
            
            for ano in range(1970, 2024):
                params = {
                    "ano": ano,
                    "subopcao": subopcao
                }
                
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
                            dados_categoria.append({
                                "subcategoria": titulo_subcategoria,
                                "ano": ano,
                                "dados": dados_linha
                            })
    
    return dados_categoria

# Inicializar a aplicação Flask
app = Flask(__name__)

# Criar uma rota para cada categoria
@app.route('/fiap/augusto/producao', methods=['GET'])
def producao():
    dados = coletar_dados(URLS['producao'])
    return jsonify(dados)

@app.route('/fiap/augusto/processamento', methods=['GET'])
def processamento():
    dados = coletar_dados(URLS['processamento'])
    return jsonify(dados)

@app.route('/fiap/augusto/comercializacao', methods=['GET'])
def comercializacao():
    dados = coletar_dados(URLS['comercializacao'])
    return jsonify(dados)

@app.route('/fiap/augusto/importacao', methods=['GET'])
def importacao():
    dados = coletar_dados(URLS['importacao'])
    return jsonify(dados)

@app.route('/fiap/augusto/exportacao', methods=['GET'])
def exportacao():
    dados = coletar_dados(URLS['exportacao'])
    return jsonify(dados)

# Executar a aplicação
if __name__ == '__main__':
    app.run(debug=True)

    