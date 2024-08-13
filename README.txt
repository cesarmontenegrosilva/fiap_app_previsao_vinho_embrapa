
# Previsão de Comercialização de Vinho Fino de Mesa (Tinto) com Prophet

Este projeto é uma aplicação web desenvolvida com Flask que utiliza o modelo Prophet para prever a comercialização de Vinho Fino de Mesa (Tinto) no Brasil. Os dados são coletados diretamente de uma API, processados, e as previsões são geradas e exibidas em um gráfico, juntamente com métricas de desempenho do modelo.

## Funcionalidades

- Coleta de dados de diferentes categorias (produção, processamento, comercialização, importação, exportação) de uma API.
- Preparação dos dados específicos de "Vinho Fino de Mesa (Tinto)" para modelagem.
- Treinamento de um modelo Prophet para previsão da comercialização de vinhos.
- Geração de previsões futuras com base nos períodos (anos) fornecidos pelo usuário.
- Avaliação do desempenho do modelo usando MAE, RMSE, R² e MAPE.
- Exibição das previsões e gráficos diretamente na interface web.

## Estrutura do Projeto

- **`app.py`**: Arquivo principal que contém toda a lógica do backend, incluindo a coleta de dados, preparação, treinamento do modelo, previsão e renderização dos resultados.
- **`requirements.txt`**: Lista de dependências do Python necessárias para rodar o projeto.
- **`templates/previsao.html`**: Arquivo HTML que define a interface web para interação com o usuário.

## Instalação

Siga as instruções abaixo para configurar e rodar o projeto localmente:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/nome-do-repositorio.git
   cd nome-do-repositorio
Crie um ambiente virtual:

bash
Copiar código
python -m venv venv
Ative o ambiente virtual:

No Windows:
bash
Copiar código
venv\Scripts\activate
No macOS/Linux:
bash
Copiar código
source venv/bin/activate
Instale as dependências:

bash
Copiar código
pip install -r requirements.txt
Execute a aplicação:

bash
Copiar código
python app.py
Acesse a aplicação:

Abra o navegador e vá para http://127.0.0.1:5000/fiap/augusto/previsao.

Uso
Na página principal, insira o número de períodos (anos) que deseja prever no campo fornecido.
Clique em "Gerar Previsão".
Veja as métricas de desempenho do modelo, as previsões detalhadas e o gráfico gerado na própria página.
Dependências
Flask
Prophet
Requests
BeautifulSoup4
Pandas
Matplotlib
Scikit-learn
NumPy
Estrutura de Diretórios
lua
Copiar código
|-- app.py
|-- requirements.txt
|-- templates
|   `-- previsao.html
|-- venv (virtual environment)
Contribuindo
Se você deseja contribuir com melhorias ou correções, siga os passos:

Fork o repositório.
Crie uma nova branch para a sua feature (git checkout -b minha-feature).
Faça as modificações e commit (git commit -am 'Adicionar nova feature').
Envie para a branch (git push origin minha-feature).
Crie um novo Pull Request.
Licença
Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para mais detalhes.

Autor
Seu Nome

bash
Copiar código

### Notas:
- **`git clone https://github.com/seu-usuario/nome-do-repositorio.git`**: Substitua o link pelo link real do seu repositório.
- **`Seu Nome`**: Substitua pelo seu nome ou usuário do GitHub.

Esse README oferece uma visão geral completa do seu projeto e deve ser útil para qualquer pessoa que queira entender, instalar ou contribuir para o projeto.


