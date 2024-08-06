#include <iostream>

int main() {
    // Declarar variáveis
    int num1, num2, soma;

    // Solicitar ao usuário para inserir o primeiro número
    std::cout << "Digite o primeiro número: ";
    std::cin >> num1;

    // Solicitar ao usuário para inserir o segundo número
    std::cout << "Digite o segundo número: ";
    std::cin >> num2;

    // Calcular a soma dos números
    soma = num1 + num2;

    // Exibir o resultado
    std::cout << "A soma de " << num1 << " e " << num2 << " é " << soma << std::endl;

    return 0;
}
