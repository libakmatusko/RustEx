from collections import defaultdict
from pprint import pp

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
        slovnik = {}
        i = -1
        self.stack = []
    def index(self, stav):
        stav = tuple(sorted(list(set(stavy))))
        if stav in slovnik:
            return slovnik[stav]
        i+=1
        slovnik[stav] = i
        self.stack.append(i)
        return i
    def pop(self):
        return self.stack.pop()


def automat_det(automat):
    m = Mapa()

    new_i = m.index(automat['starting'])
    nodes = automat['starting']
    new_node = defaultdict(def_fun)
    for n in nodes:
        for char, prechody in n.items():
            new_node[char].extend(prechody)
    for prechody in new_node.values():
        prechody = m.index(prechody)
    
    new_automat = {
        'starting': [new_i],
        'ending': [],
        'nodes': [
            defaultdict(def_fun, {'a':[1]})
        ]
    }

    return

strom = parse_or('(ab)*b*|a(a|b)|ab*|')
strom = parse_or('()a')
print(strom)
pp(automation(strom), width=100)

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
