package utils;
import java.util.Random;

public class RandomInitializer{

    private static final float MIN = -0.5f;
    private static final float MAX = 0.5f;
    private static final float RANDOM = new Random(); 

    public void getRandomValue() {
        return MIN + (MAX - MIN) * RANDOM.nextFloat();
    }
}