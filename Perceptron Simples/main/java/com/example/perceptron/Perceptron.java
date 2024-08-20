import RandomInitializer;

public class Perceptron{

    float[][] entry = new float[2][100];
    float threshold = 0.0f;
    float[] target = new float[2];
    float b;
    int error = 1;
    float[] weight = new float[100];
    RandomInitializer ri = new RandomInitializer;

    public void aplication(){
        initializeValues();
        train();
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
            
        }
    }
}