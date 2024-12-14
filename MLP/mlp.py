"""
Rafael de Oliveira Évora
MLP com AdaGrad
"""
import numpy as np
import matplotlib.pyplot as plt

# Função alvo para aproximação
def target_function(x):
    return x**2

# Obtenção do texto da função alvo diretamente do código
import inspect
funcao_alvo_str = inspect.getsource(target_function).strip().split(":")[1].strip()

# Configurações da rede neural
entradas = 1                  # Número de entradas
camadas_ocultas = [100, 50]   # Número de neurônios em cada camada oculta
alfa = 0.005                  # Taxa de aprendizado
erro_tolerado = 0.0001        # Erro máximo permitido
ciclos_maximos = 1000         # Número máximo de ciclos
xmin, xmax = -1, 1            # Domínio da função
npontos = 50                  # Número de pontos de dados
epsilon = 1e-8                # Constante para evitar divisão por zero no AdaGrad

# Gera os dados de entrada e saída
x_orig = np.linspace(xmin, xmax, npontos).reshape(-1, 1)
t_orig = target_function(x_orig)

# Configurações da rede (pesos, biases e acumuladores do AdaGrad)
camadas = [entradas] + camadas_ocultas + [1]  # Arquitetura da rede
pesos = [np.random.uniform(-0.5, 0.5, (camadas[i], camadas[i + 1])) for i in range(len(camadas) - 1)]
biases = [np.random.uniform(-0.5, 0.5, (1, camadas[i + 1])) for i in range(len(camadas) - 1)]

# Acumuladores de gradientes para AdaGrad
pesos_acumulados = [np.zeros_like(w) for w in pesos]
biases_acumulados = [np.zeros_like(b) for b in biases]

# Treinamento da rede
erro_total = 1
ciclo = 0
while erro_total > erro_tolerado and ciclo < ciclos_maximos:
    erro_total = 0
    for padrao in range(x_orig.shape[0]):
        # Forward pass
        ativacoes = [x_orig[padrao, :].reshape(1, -1)]
        for w, b in zip(pesos, biases):
            ativacoes.append(np.tanh(np.dot(ativacoes[-1], w) + b))
        y = ativacoes[-1]

        # Cálculo do erro
        erro = t_orig[padrao] - y
        erro_total += 0.5 * np.sum(erro**2)

        # Backpropagation
        grad = erro * (1 - y**2)  # Gradiente da saída
        for i in range(len(pesos) - 1, -1, -1):
            grad_w = np.dot(ativacoes[i].T, grad)
            grad_b = grad

            # Atualização dos acumuladores do AdaGrad
            pesos_acumulados[i] += grad_w**2
            biases_acumulados[i] += grad_b**2

            # Atualização dos pesos e biases com AdaGrad
            pesos[i] += (alfa * grad_w) / (np.sqrt(pesos_acumulados[i]) + epsilon)
            biases[i] += (alfa * grad_b) / (np.sqrt(biases_acumulados[i]) + epsilon)

            if i > 0:
                grad = np.dot(grad, pesos[i].T) * (1 - ativacoes[i]**2)

    ciclo += 1
    print(f"Ciclo: {ciclo} | Erro total: {erro_total:.4f}")  # Log do progresso

# Previsão final
y_final = np.zeros_like(t_orig)
for i in range(x_orig.shape[0]):
    ativacoes = [x_orig[i, :].reshape(1, -1)]
    for w, b in zip(pesos, biases):
        ativacoes.append(np.tanh(np.dot(ativacoes[-1], w) + b))
    y_final[i] = ativacoes[-1]

# Visualização dos resultados
plt.plot(x_orig, t_orig, color='red', label='Função Real')
plt.plot(x_orig, y_final, color='blue', label='Aproximação pela MLP')
plt.legend()
plt.title(f"MLP - Função Alvo: {funcao_alvo_str}")
plt.xlabel("x")
plt.ylabel("y")
plt.grid()
plt.show()
