from dataclasses import dataclass
from typing import Dict, Set, Tuple, Optional

RESULT_ACCEPTED = "Sequence accepted"
RESULT_REJECTED = "Sequence rejected"

# ========================= DFA ( #0 % 5 == 0  and  #1 % 3 == 0 ) =========================


@dataclass(frozen=True)
class DFA01:
    states: int  # 15 состояний: 5 * 3
    alphabet: Tuple[str, str]  # ('0','1')
    start: int
    finals: Set[int]
    delta: Tuple[Tuple[int, int], ...]  # [state][0|1] -> next_state

    def run(self, s: str) -> bool:
        cur = self.start
        n = len(s)
        i = 0

        while i < n:
            ch = s[i]
            if ch == self.alphabet[0]:
                cur = self.delta[cur][0]
            elif ch == self.alphabet[1]:
                cur = self.delta[cur][1]
            else:
                return False
            i += 1
        return cur in self.finals


def build_dfa_zeros_mod5_ones_mod3() -> DFA01:
    TOTAL = 5 * 3
    table = [[0, 0] for _ in range(TOTAL)]
    for i in range(5):
        for j in range(3):
            st = i * 3 + j
            next0 = ((i + 1) % 5) * 3 + j
            next1 = i * 3 + ((j + 1) % 3)
            table[st][0] = next0
            table[st][1] = next1
    finals = {0}  # (0 mod 5, 0 mod 3)
    delta_tuple = tuple((row[0], row[1]) for row in table)
    return DFA01(
        states=TOTAL, alphabet=("0", "1"), start=0, finals=finals, delta=delta_tuple
    )


# ========================= NFA ( a*  ∪  b^+ a ) =========================


@dataclass(frozen=True)
class NFA:
    # (state, symbol) -> set(next), symbol=None это ε
    trans: Dict[Tuple[int, Optional[str]], Set[int]]
    start: int
    finals: Set[int]
    alphabet: Set[str]

    def _eclosure(self, cur: Set[int]) -> Set[int]:
        stack = list(cur)
        seen = set(cur)
        while stack:
            s = stack.pop()
            for t in self.trans.get((s, None), set()):
                if t not in seen:
                    seen.add(t)
                    stack.append(t)
        return seen

    def _move(self, cur: Set[int], sym: str) -> Set[int]:
        res: Set[int] = set()
        for s in cur:
            res |= self.trans.get((s, sym), set())
        return res

    def run(self, s_: str) -> bool:
        cur = self._eclosure({self.start})
        n = len(s_)
        i = 0

        while i < n:
            ch = s_[i]
            if ch not in self.alphabet:
                return False
            cur = self._eclosure(self._move(cur, ch))
            if not cur:
                return False
            i += 1
        for q in cur:
            if q in self.finals:
                return True
        return False


def build_nfa_a_star_or_b_plus_a() -> NFA:
    # Состояния: 0=start, 1 принимает a*, 2 накапливает b+, 3 принимает финальную a
    trans: Dict[Tuple[int, Optional[str]], Set[int]] = {}

    def add(u: int, sym: Optional[str], v: int) -> None:
        key = (u, sym)
        if key in trans:
            trans[key].add(v)
        else:
            trans[key] = {v}

    add(0, None, 1)  # ε к ветке a*
    add(0, None, 2)  # ε к ветке b^+ a

    add(1, "a", 1)  # a*

    add(2, "b", 2)  # b+
    add(2, "a", 3)  # затем одна a

    return NFA(trans=trans, start=0, finals={1, 3}, alphabet={"a", "b"})


# ========================= Minimal I/O =========================


def print_minimal(seq: str, ok: bool) -> None:
    print("Input sequence:")
    print(seq)
    print(RESULT_ACCEPTED if ok else RESULT_REJECTED)


def run_console() -> None:
    dfa = build_dfa_zeros_mod5_ones_mod3()
    nfa = build_nfa_a_star_or_b_plus_a()

    print(
        "Выбор режима: введите 'dfa' (алфавит {0,1}) или 'nfa' (алфавит {a,b}). Пустая строка — выход."
    )
    while True:
        try:
            mode = input("Mode [dfa/nfa, Enter=exit]: ").strip().lower()
        except EOFError:
            return
        if mode == "":
            return
        if mode not in ("dfa", "nfa"):
            print(
                "Подсказка: напечатайте 'dfa' или 'nfa'. Пустая строка завершает программу."
            )
            continue

        if mode == "dfa":
            print(
                "Режим DFA: строки из символов '0' и '1'. Пустая строка — вернуться к выбору режима."
            )
        else:
            print(
                "Режим NFA: строки из символов 'a' и 'b'. Пустая строка — вернуться к выбору режима."
            )

        while True:
            try:
                s_ = input(
                    'Введите цепочку (Enter — назад) чтобы ввести пустую строку введите "" : '
                )

            except EOFError:
                return
            if s_ == "":
                break
            if s_ == '""':
                s_ = ""
            ok = dfa.run(s_) if mode == "dfa" else nfa.run(s_)
            print_minimal(s_, ok)


if __name__ == "__main__":
    run_console()
