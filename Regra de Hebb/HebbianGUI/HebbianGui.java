package HebbianGUI;

import javax.swing.*;
import java.awt.*;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import RuleAplication.ruleAplication;

public class HebbianGui extends JFrame {

    private final int SIZE = 10;
    private final int CELL_SIZE = 30;
    private int[][] matrix1 = new int[SIZE][SIZE];  // Matriz para armazenar os valores de seleção
    private int[][] matrix2 = new int[SIZE][SIZE];
    private int[][] testMatrix = new int[SIZE][SIZE];  // Matriz para armazenar os valores de teste
    private final JPanel matrixPanel1 = new JPanel(new GridLayout(SIZE, SIZE));
    private final JPanel matrixPanel2 = new JPanel(new GridLayout(SIZE, SIZE));
    private final JPanel testPanel = new JPanel(new GridLayout(SIZE, SIZE));
    private final JButton trainButton = new JButton("Train");
    private final JButton testButton = new JButton("Test");
    private final JButton returnButton = new JButton("Return to Training");
    private final JPanel trainingPanel = new JPanel(new GridLayout(1, 2));
    private final JPanel testPanelContainer = new JPanel(new BorderLayout());

    private boolean trained = false;  // Variável para indicar se o treinamento foi realizado
    private float[] weight;
    private float bias;
    private ruleAplication hebbRule;
    private float[] validation;

    public HebbianGui(float[][] entryLetters, ruleAplication hebbRule, float[] weight, float bias, float[] validation) {
        this.hebbRule = hebbRule;
        this.weight = weight;
        this.bias = bias;
        this.validation = validation;

        setTitle("Hebbian Learning GUI");
        setSize(900, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Inicializa os painéis
        initializePanel(matrixPanel1, matrix1);
        initializePanel(matrixPanel2, matrix2);
        initializeTestPanel();  // Inicializa o painel de teste

        // Cria o painel de treinamento
        trainingPanel.add(createPanelWithTitle("Matrix 1", matrixPanel1));
        trainingPanel.add(createPanelWithTitle("Matrix 2", matrixPanel2));

        // Cria um tabbed pane e adiciona o painel de treinamento
        JTabbedPane tabbedPane = new JTabbedPane();
        tabbedPane.addTab("Training", trainingPanel);
        add(tabbedPane, BorderLayout.CENTER);

        // Cria o painel de botões
        JPanel buttonPanel = new JPanel();
        buttonPanel.add(trainButton);
        add(buttonPanel, BorderLayout.SOUTH);

        // Adiciona action listeners
        trainButton.addActionListener(e -> {
            // Salva os dados das matrizes
            saveMatrices(entryLetters);

            // Treina o modelo com as matrizes e o bias
            hebbRule.aplication(entryLetters, bias, weight, validation);

            trained = true;  // Marca como treinado

            // Cria o painel de botões para a aba de teste
            JPanel testButtonPanel = new JPanel();
            testButtonPanel.add(testButton);
            testButtonPanel.add(returnButton);

            testPanelContainer.removeAll();
            testPanelContainer.add(createPanelWithTitle("Test Matrix", testPanel), BorderLayout.CENTER);
            testPanelContainer.add(testButtonPanel, BorderLayout.SOUTH);

            // Adiciona a aba de teste, se ainda não foi adicionada
            if (tabbedPane.getTabCount() == 1) {
                tabbedPane.addTab("Test", testPanelContainer);
            }

            // Remove o botão "Train" da tela de teste
            buttonPanel.remove(trainButton);

            // Alterna para a aba de teste
            tabbedPane.setSelectedIndex(1);
            buttonPanel.revalidate(); // Atualiza o layout para refletir as mudanças
            buttonPanel.repaint(); // Redesenha o painel
        });

        testButton.addActionListener(e -> {
            // Verifica o resultado da matriz de teste
            float[] testVector = new float[SIZE * SIZE];
            for (int i = 0; i < SIZE; i++) {
                for (int j = 0; j < SIZE; j++) {
                    testVector[i * SIZE + j] = testMatrix[i][j];
                }
            }

            // Verifica a letra reconhecida
            float result = 0;
            for (int i = 0; i < 100; i++) {
                result += testVector[i] * weight[i];
            }
            result += bias;

            String resultMessage = (result >= 0) ? "A letra desenhada corresponde à primeira letra." : "A letra desenhada corresponde à segunda letra.";

            // Exibe o resultado no popup
            JOptionPane.showOptionDialog(this,
                resultMessage,
                "Resultado do Teste",
                JOptionPane.DEFAULT_OPTION,
                JOptionPane.INFORMATION_MESSAGE,
                null,
                new Object[] { "OK" }, // Botão de fechar
                "OK");
        });

        returnButton.addActionListener(e -> {
            // Alterna de volta para a aba de treinamento
            tabbedPane.setSelectedIndex(0);

            // Readiciona o botão "Train" ao painel
            if (!buttonPanel.isAncestorOf(trainButton)) {
                buttonPanel.add(trainButton);
                buttonPanel.revalidate();
                buttonPanel.repaint();
            }
        });
    }

    private void initializePanel(JPanel panel, int[][] matrix) {
        panel.setPreferredSize(new Dimension(SIZE * CELL_SIZE, SIZE * CELL_SIZE));
        for (int i = 0; i < SIZE * SIZE; i++) {
            JButton button = new JButton();
            button.setPreferredSize(new Dimension(CELL_SIZE, CELL_SIZE));
            button.setBackground(Color.WHITE);
            button.setOpaque(true);
            button.setBorder(BorderFactory.createLineBorder(Color.BLACK));

            int row = i / SIZE;
            int col = i % SIZE;

            if (matrix != null) {  // Se houver uma matriz associada
                matrix[row][col] = -1;  // Inicializa como -1
                button.addMouseListener(new MouseAdapter() {
                    @Override
                    public void mouseClicked(MouseEvent e) {
                        JButton src = (JButton) e.getSource();
                        if (src.getBackground() == Color.BLACK) {
                            src.setBackground(Color.WHITE);
                            matrix[row][col] = -1;  // Atualiza para -1
                        } else {
                            src.setBackground(Color.BLACK);
                            matrix[row][col] = 1;  // Atualiza para 1
                        }
                    }
                });
            }
            panel.add(button);
        }
    }

    private void initializeTestPanel() {
        testPanel.setPreferredSize(new Dimension(SIZE * CELL_SIZE, SIZE * CELL_SIZE));
        for (int i = 0; i < SIZE * SIZE; i++) {
            JButton button = new JButton();
            button.setPreferredSize(new Dimension(CELL_SIZE, CELL_SIZE));
            button.setBackground(Color.WHITE);
            button.setOpaque(true);
            button.setBorder(BorderFactory.createLineBorder(Color.BLACK));

            int row = i / SIZE;
            int col = i % SIZE;

            button.addMouseListener(new MouseAdapter() {
                @Override
                public void mouseClicked(MouseEvent e) {
                    JButton src = (JButton) e.getSource();
                    if (src.getBackground() == Color.BLACK) {
                        src.setBackground(Color.WHITE);
                        testMatrix[row][col] = -1;  // Atualiza para -1
                    } else {
                        src.setBackground(Color.BLACK);
                        testMatrix[row][col] = 1;  // Atualiza para 1
                    }
                }
            });
            testPanel.add(button);
        }
    }

    private JPanel createPanelWithTitle(String title, JPanel panel) {
        JPanel container = new JPanel();
        container.setLayout(new BorderLayout());
        container.add(new JLabel(title, JLabel.CENTER), BorderLayout.NORTH);
        container.add(panel, BorderLayout.CENTER);
        return container;
    }

    private void saveMatrices(float[][] entryLetters) {
        float[] vectorA = new float[SIZE * SIZE];
        float[] vectorB = new float[SIZE * SIZE];

        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) {
                vectorA[i * SIZE + j] = matrix1[i][j];
                vectorB[i * SIZE + j] = matrix2[i][j];
            }
        }

        // Atualiza entryLetters com os valores das matrizes
        entryLetters[0] = vectorA;
        entryLetters[1] = vectorB;
    }
}
