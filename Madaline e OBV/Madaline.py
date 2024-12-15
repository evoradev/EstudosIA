import numpy as np
import tkinter as tk
from tkinter import messagebox

class Madaline:
    def __init__(self, entradas, saidas, alfa=0.1, errotolerado=0.01):
        self.entradas = entradas
        self.saidas = saidas
        self.alfa = alfa
        self.errotolerado = errotolerado
        self.limiar = 0.0

        # Pesos sinapticos e bias
        self.v = np.random.uniform(-0.1, 0.1, (entradas, saidas))
        self.v0 = np.random.uniform(-0.1, 0.1, saidas)

    def treinar(self, entAux, targAux):
        padroes = entAux.shape[0]
        erro = 1
        ciclo = 0
        max_ciclos = 30000  # Limite para evitar loops infinitos

        while erro > self.errotolerado and ciclo < max_ciclos:
            ciclo += 1
            erro = 0

            for i in range(padroes):
                padrao = entAux[i, :]
                yin = np.dot(padrao, self.v) + self.v0  # Calcula os valores de ativacao para cada saida com os pesos atuais
                y = np.where(yin >= self.limiar, 1.0, -1.0)  # Aplica a funcao de ativacao para determinar a saida

                # Atualizacao do erro
                erro += 0.5 * np.sum((targAux[i] - y) ** 2)  # Atualiza o erro acumulado com base na diferenca das saidas

                # Atualizacao dos pesos e bias
                self.v += self.alfa * np.outer(padrao, (targAux[i] - y))
                self.v0 += self.alfa * (targAux[i] - y)

            # Debugging: Mostra o progresso do treinamento
            if ciclo % 1000 == 0:
                print(f"Ciclo: {ciclo}, Erro: {erro}")

        if ciclo >= max_ciclos:
            print("Treinamento interrompido: numero maximo de ciclos atingido. Verifique os dados ou parametros de treinamento.")
        else:
            print("Treinamento concluido com sucesso.")

    def reconhecer(self, padrao):
        yin = np.dot(padrao, self.v) + self.v0
        y = np.where(yin >= self.limiar, 1.0, -1.0)
        return y

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Reconhecimento de Letras com Madaline")
        self.canvas_size = 500
        self.grid_size = 10
        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.madaline = Madaline(self.grid_size ** 2, 5)  # Maximo de 5 letras
        self.training_data = []
        self.targets = []

        # Canvas para desenho
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.canvas.bind("<Button-1>", self.draw)

        # Botoes
        self.btn_train = tk.Button(root, text="Salvar Letra", command=self.save_training_data)
        self.btn_train.grid(row=1, column=0)

        self.btn_train_all = tk.Button(root, text="Treinar", command=self.train_madaline)
        self.btn_train_all.grid(row=1, column=1)

        self.btn_recognize = tk.Button(root, text="Reconhecer Letra", command=self.recognize)
        self.btn_recognize.grid(row=1, column=2)

        self.btn_clear = tk.Button(root, text="Limpar", command=self.clear_canvas)
        self.btn_clear.grid(row=2, column=1)

    def draw(self, event):
        x, y = event.x, event.y
        size = self.canvas_size // self.grid_size
        grid_x, grid_y = x // size, y // size
        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
            if self.matrix[grid_y][grid_x] == 0:
                self.canvas.create_rectangle(grid_x * size, grid_y * size, (grid_x + 1) * size, (grid_y + 1) * size, fill="black")
                self.matrix[grid_y][grid_x] = 1
            else:
                self.canvas.create_rectangle(grid_x * size, grid_y * size, (grid_x + 1) * size, (grid_y + 1) * size, fill="white", outline="white")
                self.matrix[grid_y][grid_x] = 0

    def clear_canvas(self):
        self.canvas.delete("all")
        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)

    def save_training_data(self):
        if len(self.training_data) >= 5:
            messagebox.showinfo("Info", "Voce ja pode treinar com ate 5 letras!")
            return

        self.training_data.append(self.matrix.flatten())
        target = np.full(5, -1)
        target[len(self.training_data) - 1] = 1  # Define o alvo baseado no indice
        self.targets.append(target)

        self.clear_canvas()
        messagebox.showinfo("Info", f"Letra {chr(65 + len(self.training_data) - 1)} salva para treinamento!")

    def train_madaline(self):
        if len(self.training_data) == 0:
            messagebox.showwarning("Aviso", "Nenhuma letra foi salva para treinamento!")
            return

        self.madaline.treinar(np.array(self.training_data), np.array(self.targets))
        messagebox.showinfo("Info", "Treinamento concluido!")

    def recognize(self):
        if len(self.training_data) == 0:
            messagebox.showwarning("Aviso", "Treine a rede com pelo menos uma letra primeiro!")
            return

        padrao = self.matrix.flatten()
        y = self.madaline.reconhecer(padrao)
        letra_index = np.argmax(y)
        if y[letra_index] == 1.0:
            letra = chr(65 + letra_index)
            messagebox.showinfo("Resultado", f"A letra reconhecida e: {letra}")
        else:
            messagebox.showinfo("Resultado", "Nao foi possivel reconhecer a letra.")
        self.clear_canvas()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
