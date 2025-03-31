class TG:
    def __init__(self, alphabets, initial_states, final_states):
        self.alphabets = set(alphabets)  # Set of valid input letters
        self.initial_states = set(initial_states)  # Initial states
        self.final_states = set(final_states)  # Accepting states
        self.transitions = {}  # Dictionary to store transitions

    def Add(self, source, substring, destination):
        if source not in self.transitions:
            self.transitions[source] = []
        self.transitions[source].append((substring, destination))

    def FindPath(self, input_string, final_states):
        l = len(input_string)
        paths = []
        queue = [(state, 0, [], []) for state in self.initial_states]
        found = False
        while queue:
            state, index, path, transition_steps = queue.pop(0)
            
            if l == index and state in final_states:
                s = ")(".join(transition_steps)
                t = ")(".join(path)
                print(f"({t})")
                print(f"({s})({state})")
                print()
                found = True
                continue

            if state in self.transitions:
                for substring, next_state in self.transitions[state]:
                    sub_len = len(substring)
                    if input_string[index:index + sub_len] == substring:
                        queue.append((next_state, index + sub_len, path+[state], transition_steps+[substring]))

        if not found:
            print("No valid path found.")

def GetSample001TG() -> TG:
    print("tg = TG(['a', 'b'], ['-'], ['+'])")
    print("tg.Add('-', 'a', '1')")  
    print("tg.Add('-', 'a', '4')")
    print("tg.Add('1', 'a', '-')")  
    print("tg.Add('1', 'a', '+')")
    print("tg.Add('1', 'b', '3')")
    print("tg.Add('2', 'a', '2')")
    print("tg.Add('2', 'bb', '1')")
    print("tg.Add('2', 'bbb', '+')")
    print("tg.Add('3', 'bb', '2')")
    print("tg.Add('4', 'b', '4')")
    print("tg.Add('4', 'a', '+')")
    print("tg.Add('4', 'b', '+')")
    print("tg.Add('4', 'bbb', '1')")
    print("tg.Add('+', 'b', '+')")
    print("tg.Add('+', 'ab', '3')")

    tg = TG(['a', 'b'], ['-'], ['+'])
    tg.Add('-', 'a', '1')  
    tg.Add('-', 'a', '4')
    tg.Add('1', 'a', '-')  
    tg.Add('1', 'a', '+')
    tg.Add('1', 'b', '3')
    tg.Add('2', 'a', '2')
    tg.Add('2', 'bb', '1')
    tg.Add('2', 'bbb', '+')
    tg.Add('3', 'bb', '2')
    tg.Add('4', 'b', '4')
    tg.Add('4', 'a', '+')
    tg.Add('4', 'b', '+')
    tg.Add('4', 'bbb', '1')
    tg.Add('+', 'b', '+')
    tg.Add('+', 'ab', '3')
    return tg

def Example001(input_string='abbbabbbabba'):
    tg = GetSample001TG()
    print(f"tg.FindPath('{input_string}', ['+'])")
    tg.FindPath(input_string, ['+'])
