import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define o cabeçalho para simular um navegador ao fazer a requisição
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

def pegar_url(item):
    """Função para criar a URL de pesquisa com base no item fornecido."""
    modelo = 'https://www.pichau.com.br/search?q={}'
    url = modelo.format(item)
    return url

# Chama a função para obter a URL de pesquisa para 'gabinete'
url = pegar_url('gabinete')

# Faz a requisição GET ao site usando a URL criada
resposta = requests.get(url, headers=headers)

# Parseia o conteúdo HTML da página usando BeautifulSoup
site = BeautifulSoup(resposta.content, 'html.parser')

# Encontra todos os cards de produtos na página
card_produtos = site.find_all('div', attrs={'class': 'MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4 MuiGrid-grid-lg-3 MuiGrid-grid-xl-2'})

# Inicializa listas vazias para armazenar os nomes, preços e links dos produtos
nomes = []
precos = []
links = []

# Itera sobre cada card de produto encontrado
for card in card_produtos:
    # Encontra o elemento HTML que contém o nome do produto
    nome = card.find('h2', 'MuiTypography-root jss80 jss81 MuiTypography-h6')
    # Adiciona o texto do nome do produto à lista 'nomes'
    nomes.append(nome.text)
    
    # Encontra o elemento HTML que contém o preço do produto
    preco = card.find('div', 'jss83')
    # Adiciona o texto do preço do produto à lista 'precos'
    precos.append(preco.text)

    try:
        # Encontra o elemento HTML que contém o link do produto
        link = card.find('a', 'jss16')
        # Concatena o link base com o link encontrado e adiciona à lista 'links'
        link = 'https://www.pichau.com.br' + link['href']
        links.append(link)
        print(link)
    except RuntimeError:
        print('Erro ao pegar os links')

# Cria um dicionário com as listas de nomes, preços e links
data = {
    'Nome': nomes,
    'Preço': precos,
    'Link': links
}

# Cria um DataFrame do Pandas com os dados e sem índices
df = pd.DataFrame(data, index=None)

# Salva o DataFrame em um arquivo Excel
df.to_excel('produtos.xlsx')

# Imprime o DataFrame
print(df)
