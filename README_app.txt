# Flask API para Coleta de Dados de Uvas, Vinhos e Derivados do site da Embrapa: 

Este projeto é uma API RESTful desenvolvida em Flask que coleta dados de diferentes categorias de produção, processamento, comercialização, importação e exportação de uvas, vinhos e derivados a partir de um site específico. A API extrai informações de subcategorias existentes e retorna os dados no formato JSON.

## Funcionalidades

- **Coleta de Dados**: A API acessa páginas específicas e extrai dados tabelados para diferentes anos, desde 1970 até 2023.
- **Subcategorias**: O aplicativo identifica e coleta dados de todas as subcategorias disponíveis, como "Viníferas" e "Americanas e Híbridas".
- **API RESTful**: Cada conjunto de dados de categoria pode ser acessado por meio de rotas dedicadas, retornando os dados em formato JSON.

## Estrutura de Diretórios

├── app.py
├── requirements.txt
└── README.md

markdown
Copiar código

- `app.py`: O arquivo principal contendo o código da API.
- `requirements.txt`: Arquivo listando as dependências do projeto.
- `README.md`: Documentação do projeto.

## Requisitos

- Python 3.x
- Flask
- Requests
- BeautifulSoup4

## Instalação

1. Clone este repositório para o seu ambiente local.

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
Crie um ambiente virtual e ative-o (opcional).

bash
Copiar código
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
Instale as dependências listadas no requirements.txt.

bash
Copiar código
pip install -r requirements.txt
Uso
Execute o aplicativo Flask.

bash
Copiar código
python app.py
Acesse a API em http://127.0.0.1:5000/ com as seguintes rotas:

/fiap/augusto/producao: Coleta dados da categoria "Produção".
/fiap/augusto/processamento: Coleta dados da categoria "Processamento".
/fiap/augusto/comercializacao: Coleta dados da categoria "Comercialização".
/fiap/augusto/importacao: Coleta dados da categoria "Importação".
/fiap/augusto/exportacao: Coleta dados da categoria "Exportação".
Exemplos de Rotas
Produção
bash
Copiar código
GET /fiap/augusto/producao
Retorna dados de produção para todos os anos disponíveis e subcategorias se existir.

Processamento
bash
Copiar código
GET /fiap/augusto/processamento
Retorna dados de processamento para todos os anos disponíveis e subcategorias.

Comercialização
bash
Copiar código
GET /fiap/augusto/comercializacao
Retorna dados de comercialização para todos os anos disponíveis e subcategorias.

Notas
Este aplicativo foi configurado para funcionar localmente, mas pode ser adaptado para ser implementado em servidores remotos.
Certifique-se de que o site de onde os dados são coletados esteja acessível e que a estrutura HTML não tenha sido modificada.
Contribuição
Sinta-se à vontade para contribuir com melhorias e correções. Abra um pull request ou crie uma issue no repositório.

Licença
Este projeto é licenciado sob a Licença MIT. Consulte o arquivo LICENSE para obter mais informações.