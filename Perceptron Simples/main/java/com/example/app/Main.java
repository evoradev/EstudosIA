import javax.swing.SwingUtilities;

import PerceptronGUI;

public class Main{

    public static void main(String[] args) {

        SwingUtilities.invokeLater(() -> {
            PerceptronGUI gui = new PerceptronGUI();
            gui.setVisible(true);
        });
    }
}