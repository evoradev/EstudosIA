import javax.swing.SwingUtilities;
import HebbianGUI.HebbianGui;
import RuleAplication.ruleAplication;

public class HebbRule {

    public static void main(String[] args) {

        float[][] entryLetters = new float[2][100];
        float[] validation = new float[] { 1.0f, -1.0f };
        float[] weight = new float[100];
        float bias = 0.0f;
        ruleAplication hebbRule = new ruleAplication();

        initializeMatrix(weight, entryLetters);
        initializeGUI(entryLetters, hebbRule, weight, bias, validation);
    }

    private static void initializeMatrix(float[] weight, float[][] entryLetters) {
        for (int i = 0; i < 100; i++) {
            entryLetters[0][i] = -1;
            entryLetters[1][i] = -1;
            weight[i] = 0;
        }
    }

    private static void initializeGUI(float[][] entryLetters, ruleAplication hebbRule, float[] weight, float bias, float[] validation) {
        SwingUtilities.invokeLater(() -> {
            HebbianGui gui = new HebbianGui(entryLetters, hebbRule, weight, bias, validation);
            gui.setVisible(true);
        });
    }
}
