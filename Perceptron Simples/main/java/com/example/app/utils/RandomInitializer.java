package utils;
import java.util.Random;

public class RandomInitializer {
    private Random random;

    public RandomInitializer() {
        random = new Random();
    }

    public float getRandomValue() {
        return random.nextFloat();
    }
}