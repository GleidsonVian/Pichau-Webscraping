import tkinter as tk
from tkinter import messagebox

def salvar_produto():
    produto = entrada_produto.get()  # Obtém o texto digitado pelo usuário
    print("Produto inserido pelo usuário:", produto)
    # Aqui você pode fazer o que quiser com o produto, como salvá-lo em uma variável

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
