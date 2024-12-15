# Trabalho 7

import numpy as np
import matplotlib.pyplot as plt
import random

def funcao_objetivo(x):
    return -abs(x * np.sin(np.sqrt(abs(x))))

# Configurações do algoritmo genético
TAMANHO_POPULACAO = 50  # Quantidade de indivíduos na população
GERACOES = 100  # Número de gerações
TAXA_MUTACAO = 0.1  # Probabilidade de mutação
TAXA_CROSSOVER = 0.8  # Probabilidade de crossover
INTERVALO = (0, 512)  # Intervalo de busca da solução
BITS = 10  # Número de bits para representar cada cromossomo

# Função para inicializar a população
def inicializar_populacao(tamanho):
    return [np.random.randint(0, 2**BITS) for _ in range(tamanho)]

# Converter cromossomo binário para valor decimal
def decodificar(cromossomo):
    return INTERVALO[0] + (INTERVALO[1] - INTERVALO[0]) * (cromossomo / (2**BITS - 1))

# Função para selecionar indivíduos (seleção por torneio)
def selecao_torneio(populacao, aptidao, tamanho_torneio=3):
    selecionados = random.sample(range(len(populacao)), tamanho_torneio)
    melhor = selecionados[np.argmin([aptidao[i] for i in selecionados])]
    return populacao[melhor]

# Função de crossover (método de ponto de corte)
def crossover(pai1, pai2):
    if random.random() < TAXA_CROSSOVER:
        ponto = random.randint(1, BITS - 1)
        mascara = (1 << ponto) - 1
        filho = (pai1 & mascara) | (pai2 & ~mascara)
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
    # Inicializar a população
    populacao = inicializar_populacao(TAMANHO_POPULACAO)
    
    for geracao in range(GERACOES):
        # Avaliar a aptidão de cada indivíduo
        aptidao = np.array([funcao_objetivo(decodificar(cromossomo)) for cromossomo in populacao])
        
        # Criar nova população
        nova_populacao = []

        for _ in range(TAMANHO_POPULACAO // 2):
            # Seleção
            pai1 = selecao_torneio(populacao, aptidao)
            pai2 = selecao_torneio(populacao, aptidao)

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
    return decodificar(populacao[melhor_indice]), aptidao[melhor_indice]

# Executar o algoritmo genético
melhor_x, melhor_fx = algoritmo_genetico()
print(f"\nMelhor solucao: x = {melhor_x:.4f}, f(x) = {melhor_fx:.4f}")

# Gerar pontos para plotar a função
x_valores = np.linspace(INTERVALO[0], INTERVALO[1], 1000)
y_valores = [funcao_objetivo(x) for x in x_valores]

# Plotar a função e o ponto encontrado
plt.figure(figsize=(10, 6))
plt.plot(x_valores, y_valores, label="f(x) = -|x * sin(sqrt(|x|))|", color="blue")
plt.scatter(melhor_x, melhor_fx, color="red", label=f"Melhor solucao: x = {melhor_x:.4f}, f(x) = {melhor_fx:.4f}")
plt.title("Otimizacao de Funcao usando Algoritmo Genetico")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.axvline(melhor_x, color="green", linestyle="--", label="Melhor x")
plt.legend()
plt.grid(True)
plt.show()
