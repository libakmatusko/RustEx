from collections import defaultdict

#regex = input().strip()

'''
    // a|b    or
    // ab     join
    // a*     iterator
    // ()
    // .      hocijaky znak
'''
def_fun = lambda: -1

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
                    defaultdict(def_fun, {strom:1}),
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
            pass
        elif operator == '*':
            automat = automaty[0]
            starts = automat['starting'].copy()



    return automat

def automat_shift(automat, n):
    automat['starting'] = [x+n for x in automat['starting']]
    automat['ending'] = [x+n for x in automat['ending']]
    automat['nodes'] = [defaultdict(def_fun) for _ in range(n)] + automat['nodes']
    for node in automat['nodes']:
        for k, v in node.items():
            node[k] = v+n

strom = parse_or('(ab)*b*|a(a|b)|ab*|')
print(strom)
a = {
    'starting': [0],
    'ending': [1],
    'nodes': [
        defaultdict(def_fun, {'a':1}),
        defaultdict(def_fun)
    ]
}
automat_shift(a, 3)
print(a)

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
