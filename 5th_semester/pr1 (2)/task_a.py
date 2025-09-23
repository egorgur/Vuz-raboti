class DFA:
    def __init__(self):
        self.transitions = {
            0: {"a": 1, "b": 0},
            1: {"a": 2, "b": 1},
            2: {"a": 3, "b": 2},
            3: {"a": 4, "b": 3},
            4: {"a": 4, "b": 4},
        }
        self.initial_state = 0
        self.accept_states = {0, 1, 2, 3}

    def process(self, input_string):
        current_state = self.initial_state
        for char in input_string:
            if char not in ["a", "b"]:
                return "Reject"
            current_state = self.transitions[current_state][char]
        if current_state in self.accept_states:
            return "Accept"
        else:
            return "Reject"


dfa = DFA()

if __name__ == "__main__":
    string = input("Enter a string: ")
    result = dfa.process(string)
    print(result)
