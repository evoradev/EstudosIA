package RuleAplication;

public class ruleAplication {

    public void aplication(float[][] entryLetters, float bias, float[] weight, float[] validation){
        float[] deltaW = new float[100];
        float deltaB = 0.0f;

        for(int i = 0; i < 2; i++){

            for(int j = 0; j < 100; j++){
                deltaW[j] = entryLetters[i][j] * validation[i];
            }
            deltaB = validation[i];

            for(int j = 0; j < 100; j++){
                weight[j] = weight[j] + deltaW[j];
            }

            bias = bias + deltaB;
        }

        weightAndBiasValidation(entryLetters, weight, bias);
    }

    private static void weightAndBiasValidation (float[][] entryLetters,float[] weight, float bias){
        float deltaTeste = 0.0f;
        float[] test = new float[2];

        for(int i = 0; i < 2; i++){
            
            for(int j = 0; j < 100; j++){
                
                deltaTeste = deltaTeste + (weight[j] * entryLetters[i][j]);

            }

            deltaTeste = deltaTeste + bias;

            if(deltaTeste >= 0){
                test[i] = 1;
            }
            else{
                test[i] = -1;
            }
        }
    }
    
}
