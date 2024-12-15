# Trabalho 9

import numpy as np
import matplotlib.pyplot as plt
import random
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Configurações iniciais globais
tamanho_populacao = 100  # Quantidade de indivíduos na população
geracoes = 10000  # Número de ciclos de evolução
taxa_mutacao = 0.1  # Probabilidade de mutação
aulas_por_dia = 5  # Quantidade de aulas por dia
dias_semana = 2  # Quantidade de dias na semana
total_aulas = aulas_por_dia * dias_semana  # Total de aulas no horário
professores = 29  # Número total de professores
turmas = 3  # Número de turmas

# Função para inicializar a população garantindo que cada professor tenha ao menos um horário
def inicializar_populacao(tamanho):
    populacao = []
    for _ in range(tamanho):
        matriz = np.zeros((total_aulas, turmas), dtype=int)
        # Garantir que cada professor tenha pelo menos um horário
        for p in range(1, professores + 1):
            linha = random.randint(0, total_aulas - 1)
            coluna = random.randint(0, turmas - 1)
            matriz[linha, coluna] = p
        # Preencher os demais valores aleatoriamente
        for i in range(total_aulas):
            for j in range(turmas):
                if matriz[i, j] == 0:
                    matriz[i, j] = random.randint(1, professores)
        populacao.append(matriz)
    return populacao

# Função de aptidão: penaliza choques de horários, bonifica aulas consecutivas e verifica cobertura de professores
def funcao_aptidao(matriz):
    aptidao = 0
    professores_usados = set()
    for t in range(turmas):
        for i in range(total_aulas):
            professor = matriz[i, t]
            professores_usados.add(professor)
            # Penalizar choques de professores no mesmo horário
            if (matriz[i] == professor).sum() > 1:
                aptidao -= 5
            # Bonificar distribuição sequencial (aulas consecutivas de um professor)
            if i > 0 and matriz[i, t] == matriz[i - 1, t]:
                aptidao += 2
    # Penalizar se algum professor não tiver pelo menos um horário
    if len(professores_usados) < professores:
        aptidao -= 10 * (professores - len(professores_usados))
    return aptidao

# Função de seleção por torneio
def selecao_torneio(populacao, aptidoes, tamanho_torneio=3):
    selecionados = random.sample(range(len(populacao)), tamanho_torneio)
    melhor = selecionados[np.argmax([aptidoes[i] for i in selecionados])]
    return populacao[melhor]

# Função de crossover: troca de linhas entre matrizes (horários)
def crossover(pai1, pai2):
    filho = pai1.copy()
    if random.random() < 0.8:  # Taxa de crossover fixa
        linha = random.randint(0, total_aulas - 1)
        filho[linha] = pai2[linha]
    return filho

# Função de mutação: altera aleatoriamente o professor de uma aula
def mutacao(matriz):
    if random.random() < taxa_mutacao:
        linha = random.randint(0, total_aulas - 1)
        coluna = random.randint(0, turmas - 1)
        matriz[linha, coluna] = random.randint(1, professores)
    return matriz

# Implementação do algoritmo genético
def algoritmo_genetico():
    populacao = inicializar_populacao(tamanho_populacao)
    
    for geracao in range(geracoes):
        aptidoes = [funcao_aptidao(ind) for ind in populacao]
        nova_populacao = []
        
        for _ in range(tamanho_populacao // 2):
            pai1 = selecao_torneio(populacao, aptidoes)
            pai2 = selecao_torneio(populacao, aptidoes)
            filho1 = crossover(pai1, pai2)
            filho2 = crossover(pai2, pai1)
            nova_populacao.extend([mutacao(filho1), mutacao(filho2)])
        
        populacao = nova_populacao
        melhor_aptidao = max(aptidoes)
        print(f"Geracao {geracao + 1}: Melhor Aptidao = {melhor_aptidao}")

    aptidoes = [funcao_aptidao(ind) for ind in populacao]
    melhor_indice = np.argmax(aptidoes)
    return populacao[melhor_indice]

# Interface Gráfica
class InterfaceAG:
    def __init__(self, root):
        self.root = root
        self.root.title("Configuração do AG para Horarios")

        # Frame principal
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=1)

        # Canvas com barra de rolagem
        canvas = tk.Canvas(main_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        self.scroll_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Entradas dos parâmetros
        self.parametros = {
            "Professores": 29,
            "Turmas": 3,
            "Aulas por Dia": 5,
            "Dias da Semana": 2,
            "Tamanho da Populacao": 100,
            "Numero de Ciclos": 10000,
            "Taxa de Mutacao": 0.1
        }

        for i, (param, valor) in enumerate(self.parametros.items()):
            ttk.Label(self.scroll_frame, text=param).grid(row=i, column=0)
            entrada = ttk.Entry(self.scroll_frame)
            entrada.insert(0, str(valor))
            entrada.grid(row=i, column=1)
            self.parametros[param] = entrada
        
        # Botão iniciar
        ttk.Button(self.scroll_frame, text="Iniciar", command=self.iniciar).grid(row=len(self.parametros), column=0, columnspan=2)
        
        # Espaço para exibir o horário
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.scroll_frame)
        self.canvas.get_tk_widget().grid(row=len(self.parametros) + 1, column=0, columnspan=2)
        
    def iniciar(self):
        global tamanho_populacao, geracoes, taxa_mutacao, professores, turmas, aulas_por_dia, dias_semana, total_aulas

        # Atualizar os parâmetros
        professores = int(self.parametros["Professores"].get())
        turmas = int(self.parametros["Turmas"].get())
        aulas_por_dia = int(self.parametros["Aulas por Dia"].get())
        dias_semana = int(self.parametros["Dias da Semana"].get())
        total_aulas = aulas_por_dia * dias_semana
        tamanho_populacao = int(self.parametros["Tamanho da Populacao"].get())
        geracoes = int(self.parametros["Numero de Ciclos"].get())
        taxa_mutacao = float(self.parametros["Taxa de Mutacao"].get())

        # Executar o algoritmo
        melhor_solucao = algoritmo_genetico()
        self.plotar_matriz(melhor_solucao)

    def plotar_matriz(self, matriz):
        self.ax.clear()
        self.ax.axis('tight')
        self.ax.axis('off')
        dias = ["Sábado", "Domingo", "Segunda", "Terça", "Quarta"][:dias_semana]
        horarios = [str(i + 1) for i in range(aulas_por_dia)]
        dias_label = [f"{dias[i // aulas_por_dia]} {horarios[i % aulas_por_dia]}" for i in range(total_aulas)]
        colunas_label = [f"Turma {j + 1}" for j in range(turmas)]
        tabela = self.ax.table(cellText=matriz, loc='center', cellLoc='center', 
                               rowLabels=dias_label, colLabels=colunas_label)
        tabela.auto_set_font_size(False)
        tabela.set_fontsize(8)
        self.canvas.draw()

# Inicializar a interface gráfica
root = tk.Tk()
app = InterfaceAG(root)
root.mainloop()
