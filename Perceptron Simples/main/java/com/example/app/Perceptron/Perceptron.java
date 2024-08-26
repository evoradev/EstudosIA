import RandomInitializer;

public class Perceptron{

    float[][] entry = new float[2][100];
    float threshold = 0.0f;
    float[] target = new float[2];
    float b, alpha;
    int error = 1;
    int y, ciclo = 0;
    int i, j, limiar = 0;
    float yLiq = 0;
    float[] weight = new float[100];
    RandomInitializer ri = new RandomInitializer;

    public void aplication(){
        initializeValues();
        train();
    }

    public void testValues(){
        i = 0;
        j = 0;

        while(i < 2){
            while(j < 100){
                System.out.println("\n Entry" + [i] + [j] + ": " + entry[i][j])
                j++
            }
            i++
            System.out.println("\n")
        }

        for(i = 0; i < 2; i++){
            int test = 0;
            for(j = 0; j < 100; j++){
                test = test + (entry[i][j] * weight[j]);
            }
            test = test + b;

            if(test >= limiar){
                int yTeste = 1;
            }else{
                int yTeste = -1;
            }

            print("\n Saida da rede:" + i + ": "+ yTeste);
        }
    }

    private void initializeValues(){
        for(int i = 0; i < 100; i++){
            weight[i] = ri.getRandomValue();
        }

        b = ri.getRandomValue();
        target[0] = -1;
        target[1] = 1;
    }

    private void train(){
        while(error == 1){
            error = 0;
            i = 0
            while(i < 2)
            {
                yLiq = 0;
                j = 0;
                while(j < 100){
                    yLiq = yLiq + (entry[i][j]*weight[j]);
                    j++;
                }
                yLiq = yLiq + b; 
                if(yLiq >= limiar){
                    y = 1;
                }else{
                    y = -1;
                }
                System.out.println("\n y: " + y + "target " + target[i]);
                alpha = 0.01;

                if(y != target[i]){
                    error = 1;
                    j = 0;
                    while(j < 100){
                        weight[j] = weight[j] + (alpha * target[i] * entry[i][j]);
                        j++
                    }

                    b = b + (alpha * target[i]);
                }
                i++;   
            }
            System.out.println("\n Ciclo: " + ciclo);
            ciclo++;
        }
        System.out.println("\n Rede treinada !");
    }
}