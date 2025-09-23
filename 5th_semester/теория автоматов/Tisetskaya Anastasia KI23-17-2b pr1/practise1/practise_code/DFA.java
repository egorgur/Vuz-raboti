import java.util.Scanner;

class DFA {
    private static final int TOTAL_STATES = 15; // 5*3
    private static final int ALPHABET_CHARACTERS = 2;

    public static final int UNKNOWN_SYMBOL_ERR = 0;
    public static final int NOT_REACHED_FINAL_STATE = 1;
    public static final int REACHED_FINAL_STATE = 2;

    private static final char[] g_alphabet = {'0', '1'};
    private static final int[][] g_Transition_Table = new int[TOTAL_STATES][ALPHABET_CHARACTERS];
    private static final boolean[] g_Final_states = new boolean[TOTAL_STATES];
    private static int g_Current_state = 0; // начальное состояние (0,0)

    public static void SetDFA_Transitions() {
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 3; j++) {
                int state = i * 3 + j;
                int next0 = ((i + 1) % 5) * 3 + j; // при 0 увеличиваем остаток нулей
                int next1 = i * 3 + ((j + 1) % 3); // при 1 увеличиваем остаток единиц
                g_Transition_Table[state][0] = next0;
                g_Transition_Table[state][1] = next1;
            }
        }
        // Конечное состояние только (0,0)
        g_Final_states[0] = true;
    }

    public static int DFA(char current_symbol) {
        int pos = -1;
        for (int k = 0; k < ALPHABET_CHARACTERS; k++) {
            if (current_symbol == g_alphabet[k]) {
                pos = k;
                break;
            }
        }
        if (pos == -1) return UNKNOWN_SYMBOL_ERR;

        g_Current_state = g_Transition_Table[g_Current_state][pos];
        if (g_Final_states[g_Current_state]) return REACHED_FINAL_STATE;
        return NOT_REACHED_FINAL_STATE;
    }

    public static void Reset() {
        g_Current_state = 0; // сброс в начальное состояние
    }
}

class Main {
    public static void main(String[] args) {
        DFA.SetDFA_Transitions();

        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter a string with '0' and '1': (Press Enter to stop)");

        while (scanner.hasNextLine()) {
            String input = scanner.nextLine();
            if (input.equals("")) break;

            DFA.Reset();
            int result = DFA.NOT_REACHED_FINAL_STATE;

            for (char c : input.toCharArray()) {
                result = DFA.DFA(c);
                if (result == DFA.UNKNOWN_SYMBOL_ERR) {
                    System.out.println("Unknown symbol found. Rejected");
                    break;
                }
            }

            if (result == DFA.REACHED_FINAL_STATE) {
                System.out.println("Accepted");
            } else if (result != DFA.UNKNOWN_SYMBOL_ERR) {
                System.out.println("Rejected");
            }
        }
        scanner.close();
    }
}
