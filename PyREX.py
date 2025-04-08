from collections import defaultdict
from pprint import pp
import tkinter as tk

#regex = input().strip()

'''
    // a|b    or
    // ab     join
    // a*     iterator
    // ()
    // .      hocijaky znak
'''
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
    sub_regex.append(regex[zaciatok:])
    #print(sub_regex)
    if len(sub_regex) == 1:
        return parse_iter(sub_regex[0])
    return ['+'] + [parse_iter(x) for x in sub_regex]

def parse_iter(regex):
    if len(regex) == 0:
        return regex
    if regex[-1] == '*':
        return ['*', parse_pran(regex[:-1])]
    return parse_pran(regex)

def parse_pran(regex):
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
                automat['ending'] = aut['ending']
                if any(e in automat['starting'] for e in automat['ending']):
                    automat['starting'].extend(aut['starting'])
                    automat['starting'] = list(set(automat['starting'])) #netreba ale bojim sa

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

strom = parse_or('(ab)b')
strom = parse_or('()a')
print(strom)
pp(automation(strom), width=100)
pp(automat_det(automation(strom)), width=100)

a = {
    'starting': [0],
    'ending': [1],
    'nodes': [
        defaultdict(def_fun, {'a':[1]}),
        defaultdict(def_fun)
    ]
}
automat_shift(a, 1)
#print(a)

'''
automat: {
    strating : [],
    ending : [],
    nodes : [{
        char:index
    }]
}
'''

while False:
    string = input().strip()
    if string == 'End':
        break
