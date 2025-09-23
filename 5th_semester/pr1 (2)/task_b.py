class NFA:
    def __init__(self):
        self.transitions = {
            "q0": {
                "": "q10",
            },
            "q10": {
                "1": "q1",
                "2": "q4",
                "3": "q7",
            },
            "q1": {
                "1": "q1",
                "2": "q2",
                "3": "q3",
            },
            "q2": {
                "1": "q1",
                "2": "q2",
                "3": "q3",
            },
            "q3": {
                "1": "q1",
                "2": "q2",
                "3": "q3",
            },
            "q4": {
                "1": "q5",
                "2": "q4",
                "3": "q6",
            },
            "q5": {
                "1": "q5",
                "2": "q4",
                "3": "q6",
            },
            "q6": {
                "1": "q5",
                "2": "q4",
                "3": "q6",
            },
            "q7": {
                "1": "q9",
                "2": "q8",
                "3": "q7",
            },
            "q8": {
                "1": "q9",
                "2": "q8",
                "3": "q7",
            },
            "q9": {
                "1": "q9",
                "2": "q8",
                "3": "q7",
            },
        }
        self.initial_state = "q0"
        self.accept_states = {"q1", "q4", "q7"}

    def process(self, input_string):
        if not input_string:
            return False

        current_state = "q0"

        for i in range(len(input_string) + 1):
            if i == 0:
                current_state = self.transitions[current_state][""]
            else:
                if i > len(input_string) or (i == len(input_string) and current_state == "q10"):
                    return "Reject"
                else:
                    char = input_string[i - 1]
                    if char not in ["1", "2", "3"]:
                        return "Reject"
                    current_state = self.transitions[current_state][char]

        if current_state in self.accept_states:
            return "Accept"
        else:
            return "Reject"


nfa = NFA()

if __name__ == "__main__":
    string = input("Enter a string: ")
    result = nfa.process(string)
    print(result)
