package Perceptron.Perceptron;
import utils.RandomInitializer;

public class Perceptron {

    public float[][] entry = new float[2][100];
    float[] target = new float[2];
    public float b;
    float alpha;
    int error = 1;
    int y;
    int ciclo = 0;
    int i, j, limiar = 0;
    float yLiq = 0;
    public float[] weight = new float[100];
    RandomInitializer ri = new RandomInitializer();

    public void application() {
        initializeValues();
        train();
    }

    public void testValues() {

        for (i = 0; i < 2; i++) {
            float test = 0;
            for (j = 0; j < 100; j++) {
                test += entry[i][j] * weight[j];
            }
            test += b;

            int yTeste;
            if (test >= limiar) {
                yTeste = 1;
            } else {
                yTeste = -1;
            }

            System.out.println("\n Saida da rede [" + i + "]: " + yTeste);
        }
    }

    private void initializeValues() {
        for (int i = 0; i < 100; i++) {
            weight[i] = ri.getRandomValue();
        }

        b = ri.getRandomValue();
        target[0] = -1;
        target[1] = 1;
    }

    private void train() {
        while (error == 1) {
            error = 0;
            i = 0;
            while (i < 2) {
                yLiq = 0;
                j = 0;
                while (j < 100) {
                    yLiq += entry[i][j] * weight[j];
                    j++;
                }
                yLiq += b;
                if (yLiq >= limiar) {
                    y = 1;
                } else {
                    y = -1;
                }
                System.out.println("\n y: " + y + " target: " + target[i]);
                alpha = 0.01f;

                if (y != target[i]) {
                    error = 1;
                    j = 0;
                    while (j < 100) {
                        weight[j] += alpha * target[i] * entry[i][j];
                        j++;
                    }

                    b += alpha * target[i];
                }
                i++;
            }
            System.out.println("\n Ciclo: " + ciclo);
            ciclo++;
        }
        System.out.println("\n Rede treinada!");
    }
}
