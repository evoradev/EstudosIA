import numpy as np
import matplotlib.pyplot as plt

# Função para inicializar os pesos
def inicializar_pesos(entradas, saídas, faixa=(-0.5, 0.5)):
    return np.random.uniform(faixa[0], faixa[1], (entradas, saídas))

# Função de ativação (tangente hiperbólica)
def ativacao(x):
    return np.tanh(x)

# Derivada da função de ativação
def derivada_ativacao(x):
    return 1 - np.tanh(x)**2

# Gerar os dados de entrada e saída (função "estranha" para aproximação)
def gerar_dados(tamanho, xmin, xmax):
    x = np.linspace(xmin, xmax, tamanho).reshape(-1, 1)
    y = x**2  # Exemplo de função "estranha"
    return x, y

# AdaGrad: Atualização dos pesos
def adagrad_atualizacao(pesos, gradientes_acumulados, gradiente, alfa, epsilon=1e-8):
    gradientes_acumulados += gradiente**2
    return pesos - alfa * gradiente / (np.sqrt(gradientes_acumulados) + epsilon), gradientes_acumulados

# Configurações iniciais
entradas = 1
camadas_ocultas = [200, 100, 50, 25, 10, 5, 1]  # Número de neurônios em cada camada oculta
saídas = 1
alfa_inicial = 0.5
erro_tolerado = 1e-3
ciclos_maximos = 30000
faixa_pesos = (-0.5, 0.5)

# Dados de treinamento
x, y = gerar_dados(100, -2 * np.pi, 2 * np.pi)

# Inicializar pesos e gradientes acumulados para cada camada
pesos = []
grad_acumulados = []
tamanhos_camadas = [entradas] + camadas_ocultas + [saídas]

for i in range(len(tamanhos_camadas) - 1):
    pesos.append(inicializar_pesos(tamanhos_camadas[i], tamanhos_camadas[i + 1], faixa_pesos))
    grad_acumulados.append(np.zeros_like(pesos[-1]))

# Treinamento da rede
for ciclo in range(ciclos_maximos):
    # Exibir o ciclo atual
    print(f"Ciclo: {ciclo + 1}", end='\r')  # "\r" sobrescreve a linha para não poluir a saída

    # Forward pass
    ativacoes = [x]
    for w in pesos[:-1]:
        net = np.dot(ativacoes[-1], w)
        ativacoes.append(ativacao(net))
    
    # Saída final
    net_saida = np.dot(ativacoes[-1], pesos[-1])
    saida_final = ativacao(net_saida)

    # Cálculo do erro
    erro = y - saida_final
    erro_total = np.mean(erro**2)

    if erro_total <= erro_tolerado:
        print(f"\nConvergência atingida no ciclo {ciclo + 1}. Erro total: {erro_total}")
        break

    # Backpropagation
    gradientes = [erro * derivada_ativacao(net_saida)]
    for i in range(len(pesos) - 1, 0, -1):
        grad = np.dot(gradientes[0], pesos[i].T) * derivada_ativacao(np.dot(ativacoes[i - 1], pesos[i - 1]))
        gradientes.insert(0, grad)

    # Atualização dos pesos com AdaGrad
    for i in range(len(pesos)):
        grad_pesos = np.dot(ativacoes[i].T, gradientes[i])
        pesos[i], grad_acumulados[i] = adagrad_atualizacao(
            pesos[i], grad_acumulados[i], grad_pesos, alfa_inicial
        )

# Visualização dos resultados
plt.plot(x, y, label='Função real', color='red')
plt.plot(x, saida_final, label='Aproximação', color='blue')
plt.legend()
plt.show()
