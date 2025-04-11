from collections import defaultdict
from pprint import pp
import tkinter as tk


'''
    // a|b    or
    // ab     join
    // a*     iterator
    // ()
    // .      hocijaky znak '(a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|0|1|2|3|4|5|6|7|8|9)'
'''
CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWWYZ, "

def_fun = lambda: []
#tvarime sa ze funguje ale nefunguje
def parse_or(regex):
    sub_regex = []
    zaciatok = 0
    zatvorky = 0
    for i, char in enumerate(regex):
        if char == '|' and zatvorky == 0:
            sub_regex.append(regex[zaciatok:i])
            zaciatok = i+1
        elif char == '(':
            zatvorky += 1
        elif char == ")":
            zatvorky -= 1
    sub_regex.append(regex[zaciatok:])
    #print(sub_regex)
    if len(sub_regex) == 1:
        return parse_join(sub_regex[0])
    return ['|'] + [parse_join(x) for x in sub_regex]


def parse_join(regex):
    sub_regex = []
    zaciatok = 0
    zatvorky = 0
    for i, char in enumerate(regex[:-1]):
        if char not in '(' and regex[i+1] != '*' and zatvorky == 0:
            sub_regex.append(regex[zaciatok:i+1])
            zaciatok = i+1
        elif char == '(':
            zatvorky += 1
        elif char == ")":
            zatvorky -= 1
            if zatvorky == 0 and regex[i+1] != '*':
                sub_regex.append(regex[zaciatok:i+1])
                zaciatok = i+1
    if zatvorky!=0:
        if not(zatvorky==1 and regex[-1]==')'):
            raise BaseException("neočekávaný konec řetězce")

    sub_regex.append(regex[zaciatok:])
    #print(sub_regex)
    if len(sub_regex) == 1:
        return parse_iter(sub_regex[0])
    return ['+'] + [parse_iter(x) for x in sub_regex]

def parse_iter(regex):
    if regex == '*':
        raise BaseException("Nezadavaj hluposti, nevies pisat.")
    elif len(regex) == 0:
        return regex
    elif regex[-1] == '*':
        return ['*', parse_pran(regex[:-1])]
    return parse_pran(regex)

def parse_pran(regex):
    if regex == '.':
        return parse_pran('('+ '|'.join(CHARS) +')')
    if regex == '(':
        raise BaseException("Zly vstup '('")
    if regex.count('(') != regex.count(')'):
        raise BaseException("Zly pocet '(' alebo ')'")
    if regex[0] == '(' and regex[-1] == ')':
        return parse_or(regex[1:-1])
    return regex #uz by to malo byt len jedno pismeno


def automation(strom):
    if type(strom) == str:
        if strom == '':
            automat = {
                'starting': [0],
                'ending': [0],
                'nodes': [
                    defaultdict(def_fun)
                ]
            }
        else:
            automat = {
                'starting': [0],
                'ending': [1],
                'nodes': [
                    defaultdict(def_fun, {strom:[1]}),
                    defaultdict(def_fun)
                ]
            }
    else: #je to list
        operator = strom[0]
        automaty = [automation(x) for x in strom[1:]]
        if operator == "|":
            automat = automaty[0]
            for i in range(len(automaty)-1):
                n = len(automat['nodes'])
                automat_shift(automaty[i+1], n)
                automat['starting'].extend(automaty[i+1]['starting'])
                automat['ending'].extend(automaty[i+1]['ending'])
                automat['nodes'].extend(automaty[i+1]['nodes'][n:])

        elif operator == '+':
            automat = automaty[0]
            for aut in automaty[1:]:
                n = len(automat['nodes'])
                automat_shift(aut, n)
                for node in automat['nodes']:
                    for znak, cesty in node.items():
                        if any(e in cesty for e in automat['ending']):
                            node[znak].extend(aut['starting'])
                            node[znak] = list(set(node[znak]))
                automat['nodes'].extend(aut['nodes'][n:])
                if any(e in automat['starting'] for e in automat['ending']):
                    automat['starting'].extend(aut['starting'])
                    automat['starting'] = list(set(automat['starting'])) #netreba ale bojim sa
                automat['ending'] = aut['ending']

        elif operator == '*':
            automat = automaty[0]
            automat['ending'].extend(automat['starting'])
            automat['ending'] = set(automat['ending'])
            automat['ending'] = list(automat['ending'])
            for node in automat['nodes']:
                for znak, cesty in node.items():
                    if any(e in cesty for e in automat['ending']):
                        node[znak].extend(automat['starting'])
                        node[znak] = list(set(node[znak]))

    return automat

def automat_shift(automat, n):
    automat['starting'] = [x+n for x in automat['starting']]
    automat['ending'] = [x+n for x in automat['ending']]
    automat['nodes'] = [defaultdict(def_fun) for _ in range(n)] + automat['nodes']
    for node in automat['nodes']:
        for k, v in node.items():
            node[k] = [x+n for x in v]


class Mapa:
    def __init__(self):
        self.slovnik = {}
        self.reverse = []
        self.i = -1
        self.stack = []

    def index(self, stav):
        stav = tuple(sorted(list(set(stav))))
        if stav in self.slovnik:
            return self.slovnik[stav]
        self.i+=1
        self.slovnik[stav] = self.i
        self.reverse.append(stav)
        self.stack.append(self.i)
        return self.i

    def rev(self, index):
        return self.reverse[index]

    def pop(self):
        return self.stack.pop()

    def empty(self):
        return not bool(self.stack)


def automat_det(automat):
    m = Mapa()
    new_automat = {
        'starting': [m.index(automat['starting'])],
        'ending': [],
        'nodes': []
    }

    m.index(automat['starting'])
    while not m.empty():
        #pp(new_automat, width=300)
        new_i = m.pop()
        nodes = m.rev(new_i)
        new_node = defaultdict(def_fun)
        for n_i in nodes:
            n = automat['nodes'][n_i]
            for char, prechody in n.items():
                new_node[char].extend(prechody)
        for char in new_node.keys():
            new_node[char] = m.index(new_node[char])

        if len(new_automat['nodes']) <= new_i:
            new_automat['nodes'] +=  [None for _ in range(new_i-len(new_automat['nodes'])+1)]
        new_automat['nodes'][new_i] = new_node.copy()
    
    for i in range(len(new_automat['nodes'])):
        if any([x in automat['ending'] for x in m.rev(i)]):
            new_automat['ending'].append(i)

    return new_automat

class StateGen:
    def __init__(self):
        self.next_state = 0
        self.states = {}
        self.index_to_states = []
    
    def get_state(self, states_tuple):
        if states_tuple in self.states:
            return self.states[states_tuple]
        self.states[states_tuple] = self.next_state
        self.index_to_states.append(states_tuple)
        self.next_state += 1
        return self.next_state-1
    
    def get_edges(self, state_i):
        edges = {}
        for char, next_state in zip(CHARS, self.index_to_states[state_i][1:]):
            if next_state != -1:
                edges[char] = next_state
        return edges


def automat_min(automat):
    states_groups = [int(i in automat['ending']) for i in range(len(automat['nodes']))]
    new_states_group = []
    while True:
        group_gen = StateGen()
        for i, node in enumerate(automat['nodes']):
            changes = [states_groups[i]]
            for char in CHARS:
                next_node = node[char]
                if next_node == []:
                    changes.append(-1)
                else:
                    changes.append(states_groups[next_node])
            changes = tuple(changes)
            new_states_group.append(group_gen.get_state(changes))
        
        if states_groups == new_states_group:
            new_states = set(states_groups)
            return {
                'starting':[states_groups[automat['starting'][0]]],
                'ending':list(set([states_groups[x] for x in automat['starting']])),
                'nodes':[defaultdict(def_fun, group_gen.get_edges(s)) for s in range(len(new_states))]
            }

        states_groups = new_states_group


strom = parse_or('(a|bc)*')
automat = automation(strom)
det_automat = automat_det(automat)
pp(det_automat, width=300)
min_automat = automat_min(det_automat)
pp(min_automat, width=300)

def is_valid(string, automat):
    n_i = automat['starting'][0]
    for char in string:
        new_i = automat['nodes'][n_i][char]
        if new_i == []:
            return False
        n_i = new_i
    if n_i in automat['ending']:
        return True
    return False


if False:
    vygen_automat = {}
    def gen():
        global vygen_automat
        try:
            print(entry.get())
            vygen_automat = automat_det(automation(parse_or(entry.get())))
            generation_status_label.config(text="Generation completed!")
        except BaseException as x:
            generation_status_label.config(text=x)


    def validate():
        try:
            print(text_input.get("1.0", tk.END))
            valid = is_valid(text_input.get("1.0", tk.END)[:-1], vygen_automat)
            if valid:
                result_label.config(text="Vyhovuje!")
            else:
                result_label.config(text="Nevyhovuje :(")
        except:
            result_label.config(text='Zadavaj validny text.')
    # Create main window
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.title("Your App")
    root.configure(padx=20, pady=20)
    def exit_fullscreen(event=None):
        root.attributes("-fullscreen", False)
    root.bind("<Escape>", exit_fullscreen)

    # Input field
    entry_label = tk.Label(root, text="Input:")
    entry_label.pack(anchor='w')
    entry = tk.Entry(root, width=40)
    entry.pack(pady=(0, 10))

    # Generate button
    generate_button = tk.Button(root, text="Generate", command=gen)
    generate_button.pack(pady=(0, 20))

    generation_status_label = tk.Label(root, text="", fg="green")
    generation_status_label.pack(pady=(0, 10))

    # Text widget
    text_label = tk.Label(root, text="Text Input:")
    text_label.pack(anchor='w')
    text_input = tk.Text(root, height=20, width=150)
    text_input.pack(pady=(0, 10))

    # Verify button
    verify_button = tk.Button(root, text="Verify", command=validate)
    verify_button.pack(pady=(0, 20))

    # Result label
    result_label = tk.Label(root, text="Answer will appear here", fg="blue")
    result_label.pack()

    # Start the app
    root.mainloop()
