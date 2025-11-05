class PDA:
    def __init__(self):
        """Метод инициализации PDA"""
        self.current_state = 'q0'
        self.stack = ['Z']
        self.input_index = 0
        
        self.transitions = {
            ('q0', 'a', 'A'): [('q0'), ('A', 'A')],
            ('q0', 'b', 'B'): [('q0'), ('B', 'B')],
            ('q0', 'b', 'Z'): [('q0'), ('B', 'Z')],
            ('q0', '', 'B'):  [('q1'), ('B')],
            ('q0', 'a', 'Z'): [('q0'), ('A', 'Z')],
            ('q0', 'a', 'B'): [('q0'), ('')],
            ('q0', 'b', 'A'): [('q0'), ('')]
        }
        
        self.final_states = {'q1'}
    
    def try_transit(self, symbol):
        """Метод для совершения перехода"""
        if (self.current_state, symbol, self.stack[-1]) in self.transitions:
            new_state, new_symbols = self.transitions[(self.current_state, symbol, self.stack[-1])]
            self.current_state = new_state
            if new_symbols:
                self.stack_pop()
                self.stack_push(new_symbols)
            else:
                self.stack_pop()
            return True
        return False
    
    def stack_push(self, symbols):
        """Метод для добавления символов в стек"""
        for symbol in symbols[::-1]:
            self.stack.append(symbol)
    
    def stack_pop(self):
        """Метод для удаления символов из стека"""
        self.stack.pop()

if __name__ == '__main__':
    while True:
        pda = PDA()
        test_string = input('Enter a string or "exit" to exit:')
        flag = True
        if test_string == 'exit':
            break
        else:
            for symbol in test_string:
                if pda.try_transit(symbol):
                    continue
                else:
                    flag = False
                    break
            if flag:
                pda.try_transit('')
                if pda.current_state in pda.final_states:
                    print('Accept')
                else:
                    print('Reject')
            else:
                print('Reject')
