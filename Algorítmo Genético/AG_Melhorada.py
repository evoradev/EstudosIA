# Trabalho 8

import numpy as np
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk

# Definir a função objetivo
def funcao_objetivo(x):
    return -abs(x * np.sin(np.sqrt(abs(x))))

# Configurações iniciais globais
TAMANHO_POPULACAO = 50  # Quantidade de indivíduos na população
GERACOES = 100  # Número de gerações
TAXA_MUTACAO = 0.1  # Probabilidade de mutação
TAXA_CROSSOVER = 0.8  # Probabilidade de crossover
INTERVALO = (0, 512)  # Intervalo de busca da solução
BITS = 10  # Número de bits para representar cada cromossomo
METODO_SELECAO = "torneio"  # Método de seleção (roleta ou torneio)
TAMANHO_TORNEIO = 3  # Tamanho do torneio
CROSSOVER_TIPO = "um_ponto"  # Tipo de crossover (um ponto ou dois pontos)

# Função para inicializar a população
def inicializar_populacao(tamanho):
    return [np.random.randint(0, 2**BITS) for _ in range(tamanho)]

# Converter cromossomo binário para valor decimal
def decodificar(cromossomo):
    return INTERVALO[0] + (INTERVALO[1] - INTERVALO[0]) * (cromossomo / (2**BITS - 1))

# Função de seleção por torneio
def selecao_torneio(populacao, aptidao, tamanho_torneio):
    selecionados = random.sample(range(len(populacao)), tamanho_torneio)
    melhor = selecionados[np.argmin([aptidao[i] for i in selecionados])]
    return populacao[melhor]

# Função de seleção por roleta
def selecao_roleta(populacao, aptidao):
    soma_aptidao = sum(aptidao)
    roleta = [apt / soma_aptidao for apt in aptidao]
    acumulada = np.cumsum(roleta)
    r = random.random()
    for i, prob in enumerate(acumulada):
        if r <= prob:
            return populacao[i]

# Função de crossover (um ou dois pontos)
def crossover(pai1, pai2):
    if random.random() < TAXA_CROSSOVER:
        if CROSSOVER_TIPO == "um_ponto":
            ponto = random.randint(1, BITS - 1)
            mascara = (1 << ponto) - 1
            filho = (pai1 & mascara) | (pai2 & ~mascara)
            return filho
        elif CROSSOVER_TIPO == "dois_pontos":
            ponto1 = random.randint(1, BITS - 2)
            ponto2 = random.randint(ponto1 + 1, BITS - 1)
            mascara1 = (1 << ponto1) - 1
            mascara2 = ((1 << ponto2) - 1) ^ mascara1
            filho = (pai1 & mascara1) | (pai2 & mascara2) | (pai1 & ~mascara2)
            return filho
    return pai1

# Função de mutação (aplicada apenas aos filhos)
def mutacao(cromossomo):
    if random.random() < TAXA_MUTACAO:
        bit = random.randint(0, BITS - 1)
        cromossomo ^= (1 << bit)  # Inverter o bit selecionado
    return cromossomo

# Implementação do algoritmo genético
def algoritmo_genetico():
    global TAMANHO_POPULACAO, GERACOES, METODO_SELECAO, TAMANHO_TORNEIO

    # Inicializar a população
    populacao = inicializar_populacao(TAMANHO_POPULACAO)

    for geracao in range(GERACOES):
        # Avaliar a aptidão de cada indivíduo
        aptidao = np.array([funcao_objetivo(decodificar(cromossomo)) for cromossomo in populacao])

        # Criar nova população
        nova_populacao = []

        for _ in range(TAMANHO_POPULACAO // 2):
            # Seleção
            if METODO_SELECAO == "torneio":
                pai1 = selecao_torneio(populacao, aptidao, TAMANHO_TORNEIO)
                pai2 = selecao_torneio(populacao, aptidao, TAMANHO_TORNEIO)
            elif METODO_SELECAO == "roleta":
                pai1 = selecao_roleta(populacao, aptidao)
                pai2 = selecao_roleta(populacao, aptidao)

            # Crossover
            filho1 = crossover(pai1, pai2)
            filho2 = crossover(pai2, pai1)

            # Mutação
            filho1 = mutacao(filho1)
            filho2 = mutacao(filho2)

            nova_populacao.extend([filho1, filho2])

        populacao = nova_populacao

        # Melhor solução da geração atual
        aptidao = np.array([funcao_objetivo(decodificar(cromossomo)) for cromossomo in populacao])
        melhor_indice = np.argmin(aptidao)
        melhor_solucao = decodificar(populacao[melhor_indice])
        melhor_aptidao = aptidao[melhor_indice]

        print(f"Geracao {geracao + 1}: Melhor x = {melhor_solucao:.4f}, f(x) = {melhor_aptidao:.4f}")

    # Retornar a melhor solução encontrada
    melhor_indice = np.argmin(aptidao)
    melhor_solucao = decodificar(populacao[melhor_indice])
    melhor_aptidao = aptidao[melhor_indice]

    # Plotar o gráfico com o ponto encontrado
    x_valores = np.linspace(INTERVALO[0], INTERVALO[1], 1000)
    y_valores = [funcao_objetivo(x) for x in x_valores]

    plt.figure(figsize=(10, 6))
    plt.plot(x_valores, y_valores, label="f(x) = -|x * sin(sqrt(|x|))|", color="blue")
    plt.scatter(melhor_solucao, melhor_aptidao, color="red", label=f"Melhor solução: x = {melhor_solucao:.4f}, f(x) = {melhor_aptidao:.4f}")
    plt.title("Otimizacao de Funcao usando Algoritmo Genetico")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.axvline(melhor_solucao, color="green", linestyle="--", label="Melhor x")
    plt.legend()
    plt.grid(True)
    plt.show()

    return melhor_solucao, melhor_aptidao

# Interface Gráfica
class InterfaceAG:
    def __init__(self, root):
        self.root = root
        self.root.title("Configurações do Algoritmo Genetico")

        # Campos de entrada para os parâmetros
        ttk.Label(root, text="Tamanho do Cromossomo (bits)").grid(row=0, column=0)
        self.bits_entry = ttk.Entry(root)
        self.bits_entry.insert(0, str(BITS))
        self.bits_entry.grid(row=0, column=1)

        ttk.Label(root, text="Tamanho da Populacao").grid(row=1, column=0)
        self.populacao_entry = ttk.Entry(root)
        self.populacao_entry.insert(0, str(TAMANHO_POPULACAO))
        self.populacao_entry.grid(row=1, column=1)

        ttk.Label(root, text="Taxa de Crossover").grid(row=2, column=0)
        self.crossover_entry = ttk.Entry(root)
        self.crossover_entry.insert(0, str(TAXA_CROSSOVER))
        self.crossover_entry.grid(row=2, column=1)

        ttk.Label(root, text="Taxa de Mutacao").grid(row=3, column=0)
        self.mutacao_entry = ttk.Entry(root)
        self.mutacao_entry.insert(0, str(TAXA_MUTACAO))
        self.mutacao_entry.grid(row=3, column=1)

        ttk.Label(root, text="Numero de Geracoes").grid(row=4, column=0)
        self.geracoes_entry = ttk.Entry(root)
        self.geracoes_entry.insert(0, str(GERACOES))
        self.geracoes_entry.grid(row=4, column=1)

        ttk.Label(root, text="Metodo de Selecao").grid(row=5, column=0)
        self.metodo_selecao = ttk.Combobox(root, values=["torneio", "roleta"])
        self.metodo_selecao.set(METODO_SELECAO)
        self.metodo_selecao.grid(row=5, column=1)

        ttk.Label(root, text="Tamanho do Torneio").grid(row=6, column=0)
        self.torneio_entry = ttk.Entry(root)
        self.torneio_entry.insert(0, str(TAMANHO_TORNEIO))
        self.torneio_entry.grid(row=6, column=1)

        ttk.Label(root, text="Tipo de Crossover").grid(row=7, column=0)
        self.crossover_tipo = ttk.Combobox(root, values=["um_ponto", "dois_pontos"])
        self.crossover_tipo.set(CROSSOVER_TIPO)
        self.crossover_tipo.grid(row=7, column=1)

        # Botão para iniciar o algoritmo
        ttk.Button(root, text="Iniciar", command=self.iniciar).grid(row=8, column=0, columnspan=2)

    def iniciar(self):
        global TAMANHO_POPULACAO, GERACOES, TAXA_MUTACAO, TAXA_CROSSOVER, BITS, METODO_SELECAO, TAMANHO_TORNEIO, CROSSOVER_TIPO
        
        # Atualizar os parâmetros com base nas entradas
        BITS = int(self.bits_entry.get())
        TAMANHO_POPULACAO = int(self.populacao_entry.get())
        TAXA_CROSSOVER = float(self.crossover_entry.get())
        TAXA_MUTACAO = float(self.mutacao_entry.get())
        GERACOES = int(self.geracoes_entry.get())
        METODO_SELECAO = self.metodo_selecao.get()
        TAMANHO_TORNEIO = int(self.torneio_entry.get())
        CROSSOVER_TIPO = self.crossover_tipo.get()

        # Executar o algoritmo genético
        melhor_x, melhor_fx = algoritmo_genetico()
        print(f"\nMelhor solucao: x = {melhor_x:.4f}, f(x) = {melhor_fx:.4f}")

# Inicializar a interface gráfica
root = tk.Tk()
app = InterfaceAG(root)
root.mainloop()
