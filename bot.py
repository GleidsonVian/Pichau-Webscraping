import tkinter as tk
from tkinter import messagebox
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
    print(f"Arquivo '{nome_do_arquivo_excel}.csv' criado com sucesso!")

def salvar_produto():
    produto = entrada_produto.get()  # Obtém o texto digitado pelo usuário
    print("Produto inserido pelo usuário:", produto)
    # Aqui você pode fazer o que quiser com o produto, como salvá-lo em uma variável

    # Aqui vou chamar a função para raspar os dados
    url = pegar_url(produto)
    nomes, precos, links = raspar_dados(url)
    nome_do_arquivo_excel = produto
    criar_arquivo_excel(nomes, precos, links, nome_do_arquivo_excel)

def sair():
    if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
        janela.destroy()

# Cria a janela principal
janela = tk.Tk()

# Cria o primeiro Label e a entrada para o produto
tk.Label(janela, text="Produto:").grid(column=0, row=0)
entrada_produto = tk.Entry(janela)
entrada_produto.grid(column=1, row=0)

# Cria o botão para salvar o produto
botao_produto = tk.Button(janela, text="Raspar Produto", command=salvar_produto)
botao_produto.grid(column=2, row=0)

# Cria o botão para sair
botao_sair = tk.Button(janela, text="Sair", command=sair)
botao_sair.grid(column=0, row=1, columnspan=3, pady=10)

# Inicia o loop principal
janela.mainloop()
