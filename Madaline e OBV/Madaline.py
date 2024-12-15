import numpy as np
import random as rd
import tkinter as tk
from tkinter import messagebox

# Configuração da Madaline
class Madaline:
    def __init__(self, entradas, saidas, alfa=0.1, errotolerado=0.01):
        self.entradas = entradas
        self.saidas = saidas
        self.alfa = alfa
        self.errotolerado = errotolerado
        self.limiar = 0.0

        # Pesos sinápticos e bias
        self.v = np.random.uniform(-0.1, 0.1, (entradas, saidas))
        self.v0 = np.random.uniform(-0.1, 0.1, saidas)

    def treinar(self, entAux, targAux):
        padroes = entAux.shape[0]
        erro = 1
        ciclo = 0
        max_ciclos = 10000 

        while erro > self.errotolerado and ciclo < max_ciclos:
            ciclo += 1
            erro = 0

            for i in range(padroes):
                padrao = entAux[i, :] 
                yin = np.dot(padrao, self.v) + self.v0  # Calcula os valores de ativação para cada saída com os pesos atuais
                y = np.where(yin >= self.limiar, 1.0, -1.0)  # Aplica a função de ativação para determinar a saída

                # Atualização do erro
                erro += 0.5 * np.sum((targAux[i] - y) ** 2)  # Atualiza o erro acumulado com base na diferença das saídas

                # Atualização dos pesos e bias
                for m in range(self.entradas):
                    for n in range(self.saidas):
                        self.v[m][n] += self.alfa * (targAux[i][n] - y[n]) * padrao[m]  # Ajusta o peso sináptico com base no erro local
                for n in range(self.saidas):
                    self.v0[n] += self.alfa * (targAux[i][n] - y[n])  # Ajusta o bias para a saída correspondente

            # Debugging: Mostra o progresso do treinamento
            print(f"Ciclo: {ciclo}, Erro: {erro}")

        if ciclo >= max_ciclos:
            print("Treinamento interrompido: número máximo de ciclos atingido. Verifique os dados ou parâmetros de treinamento.")
            print("Treinamento interrompido: número máximo de ciclos atingido.")
        else:
            print("Treinamento concluído com sucesso.")

    def reconhecer(self, padrao):
        """
        Reconhece o padrão fornecido com base nos pesos e bias treinados.
        Retorna a saída ativa mais forte (letra reconhecida).
        """
        yin = np.dot(padrao, self.v) + self.v0
        y = np.where(yin >= self.limiar, 1.0, -1.0)
        return y


# Interface gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento de Letras com Madaline")
        self.canvas_size = 500
        self.grid_size = 10
        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.madaline = Madaline(self.grid_size ** 2, 5)  # Máximo de 5 letras
        self.training_data = []
        self.targets = []

        # Canvas para desenho
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.canvas.bind("<B1-Motion>", self.draw)

        # Botões
        self.btn_train = tk.Button(root, text="Salvar Letra", command=self.save_training_data)
        self.btn_train.grid(row=1, column=0)

        self.btn_train_all = tk.Button(root, text="Treinar", command=self.train_madaline)
        self.btn_train_all.grid(row=1, column=1)

        self.btn_recognize = tk.Button(root, text="Reconhecer Letra", command=self.recognize)
        self.btn_recognize.grid(row=1, column=2)

        self.btn_clear = tk.Button(root, text="Limpar", command=self.clear_canvas)
        self.btn_clear.grid(row=2, column=1)

    def draw(self, event):
        """Desenha ou apaga no canvas e atualiza a matriz com debounce para evitar piscadas."""
        x, y = event.x, event.y
        size = self.canvas_size // self.grid_size
        grid_x, grid_y = x // size, y // size
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            # Adiciona debounce para evitar múltiplas ações rápidas
            if hasattr(self, 'last_toggled') and self.last_toggled == (grid_x, grid_y):
                return

            self.last_toggled = (grid_x, grid_y)

            # Alterna o estado do bloco entre 1 e 0
            if self.matrix[grid_y][grid_x] == 0:
                self.canvas.create_rectangle(grid_x * size, grid_y * size,
                                             (grid_x + 1) * size, (grid_y + 1) * size, fill="black")
                self.matrix[grid_y][grid_x] = 1
            else:
                self.canvas.create_rectangle(grid_x * size, grid_y * size,
                                             (grid_x + 1) * size, (grid_y + 1) * size, fill="white", outline="white")
                self.matrix[grid_y][grid_x] = 0

    def clear_canvas(self):
        """Limpa o canvas e reseta a matriz."""
        self.canvas.delete("all")
        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)

    def save_training_data(self):
        """Salva a matriz desenhada como padrão de treinamento."""
        if len(self.training_data) >= 5:
            messagebox.showinfo("Info", "Você já pode treinar com até 5 letras!")
            return

        self.training_data.append(self.matrix.flatten())
        target = np.zeros(5)
        target[len(self.training_data) - 1] = 1.0  # A saída é baseada no índice
        self.targets.append(target)

        self.clear_canvas()
        messagebox.showinfo("Info", f"Letra {chr(65 + len(self.training_data) - 1)} salva para treinamento!")

    def train_madaline(self):
        """Treina a Madaline com os padrões salvos."""
        if len(self.training_data) == 0:
            messagebox.showwarning("Aviso", "Nenhuma letra foi salva para treinamento!")
            return

        self.madaline.treinar(np.array(self.training_data), np.array(self.targets))
        messagebox.showinfo("Info", "Treinamento concluído!")

    def recognize(self):
        """Reconhece a letra desenhada."""
        if len(self.training_data) == 0:
            messagebox.showwarning("Aviso", "Treine a rede com pelo menos uma letra primeiro!")
            return

        padrao = self.matrix.flatten()
        y = self.madaline.reconhecer(padrao)
        letra_index = np.argmax(y)
        if y[letra_index] == 1.0:  # Verifica se é reconhecível
            letra = chr(65 + letra_index)  # Converte índice para letra (A=65, B=66, ...)
            messagebox.showinfo("Resultado", f"A letra reconhecida é: {letra}")
        else:
            messagebox.showinfo("Resultado", "Não foi possível reconhecer a letra.")
        self.clear_canvas()


# Execução do programa
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
