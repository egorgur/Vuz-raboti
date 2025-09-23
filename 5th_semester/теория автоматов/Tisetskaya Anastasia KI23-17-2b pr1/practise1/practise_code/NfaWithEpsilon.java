import java.util.*;

public class NfaWithEpsilon {
    private static final int Q0 = 0;
    private static final int Q1 = 1;
    private static final int Q2 = 2;
    private static final int Q3 = 3;

    private static final Set<Integer> FINAL_STATES = Set.of(Q1, Q3);

    private final Map<Integer, Map<Character, Set<Integer>>> trans = new HashMap<>();

    public NfaWithEpsilon() {
        for (int s = 0; s <= 3; s++) trans.put(s, new HashMap<>());

        addTransition(Q0, (char)0, Q1);
        addTransition(Q0, (char)0, Q2);

        addTransition(Q1, 'a', Q1);

        addTransition(Q2, 'b', Q2);
        addTransition(Q2, 'a', Q3);
    }

    private void addTransition(int from, char symbol, int to) {
        trans.get(from).computeIfAbsent(symbol, k -> new HashSet<>()).add(to);
    }

    private Set<Integer> epsilonClosure(Set<Integer> states) {
        Deque<Integer> stack = new ArrayDeque<>(states);
        Set<Integer> closure = new HashSet<>(states);

        while (!stack.isEmpty()) {
            int s = stack.pop();
            Set<Integer> epsNext = trans.get(s).get((char)0);
            if (epsNext == null) continue;
            for (int nx : epsNext) {
                if (closure.add(nx)) stack.push(nx);
            }
        }
        return closure;
    }

    private Set<Integer> move(Set<Integer> states, char symbol) {
        Set<Integer> result = new HashSet<>();
        for (int s : states) {
            Set<Integer> nxt = trans.get(s).get(symbol);
            if (nxt != null) result.addAll(nxt);
        }
        return result;
    }

    public boolean accepts(String input) {
        Set<Integer> current = epsilonClosure(Set.of(Q0));

        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            if (c != 'a' && c != 'b') return false;

            Set<Integer> afterMove = move(current, c);
            current = epsilonClosure(afterMove);

            if (current.isEmpty()) return false;
        }

        for (int s : current) if (FINAL_STATES.contains(s)) return true;
        return false;
    }

    public static void main(String[] args) {
        NfaWithEpsilon nfa = new NfaWithEpsilon();
        Scanner sc = new Scanner(System.in);
        System.out.println("Введите строку из {a,b}. Нажмите q для выхода.");

        while (true) {
            String line = sc.nextLine();
            if (line.equals("q")) break;

            boolean ok = nfa.accepts(line);
            System.out.println(ok ? "Accepted" : "Rejected");
        }
        sc.close();
    }
}
