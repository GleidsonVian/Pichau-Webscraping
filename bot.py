import requests
from bs4 import BeautifulSoup
import pandas as pd


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

def pegar_url(item):
    modelo = 'https://www.pichau.com.br/search?q={}'
    return modelo.format(item)

def raspar_dados(url):
    nomes = []
    precos = []
    links = []

    resposta = requests.get(url, headers=headers)
    site = BeautifulSoup(resposta.content, 'html.parser')
    card_produtos = site.find_all('div', class_='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12 MuiGrid-grid-sm-6 MuiGrid-grid-md-4 MuiGrid-grid-lg-3 MuiGrid-grid-xl-2')

    for card in card_produtos:
        try:
            nome = card.find('h2', class_='MuiTypography-root jss80 jss81 MuiTypography-h6').text.strip()
            nomes.append(nome)
        except AttributeError:
            nomes.append('Nome não encontrado')

        try:
            preco = card.find('div', class_='jss83').text.strip()
            precos.append(preco)
        except AttributeError:
            precos.append('Preço não encontrado')

        try:
            link = 'https://www.pichau.com.br' + card.find('a')['href']
            links.append(link)
        except (AttributeError, TypeError):
            links.append('Link não encontrado')

    return nomes, precos, links

def criar_arquivo_excel(nomes, precos, links, nome_do_arquivo_excel):
    data = {'Nome': nomes, 'Preço': precos, 'Link': links}
    df = pd.DataFrame(data)
    df.to_excel(f'{nome_do_arquivo_excel}.xlsx', index=False)
    print(f"Arquivo '{nome_do_arquivo_excel}.xlsx' criado com sucesso!")

def main():
    item = input('Escolha um item para ser raspado informações: ')
    url = pegar_url(item)
    nomes, precos, links = raspar_dados(url)
    nome_do_arquivo_excel = input('Qual o nome para o arquivo excel atual? ')
    criar_arquivo_excel(nomes, precos, links,nome_do_arquivo_excel)

if __name__ == "__main__":
    main()

