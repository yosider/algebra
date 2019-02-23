class Node():
    def __init__(self, children=[], value=None, name=''):
        #TODO: type checking
        self.children = list(children)
        self.name = name
        self.value = value

    def evaluate(self, dic={}):
        s = self.assign(dic) if dic else self
        s = s.operate()  # 係数表現
        s = self.coeff2str(s)  # 係数表現の文字列
        print(s)

    def coeff2str(self, dic):
        string = ''
        variables = sorted(dic)[::-1]
        for var in variables:
            coeff = dic[var]

            # 符号の文字列
            if coeff > 0:
                sign = ' + ' if string else ''  # 先頭の+符号は書かない
            elif coeff == 0:
                continue  # 係数が0の項は無視
            else:
                sign = ' -'  # 負号はくっつける

            # 変数名の文字列
            var = var if var!='1' else ''  # 定数は変数名なし

            # 係数の文字列
            coeff = str(abs(coeff)) if abs(coeff)!=1 or not var else ''  # 係数1は書かない，ただし定数項の1は書く
            
            string += sign + coeff + var
        return string


class Constant(Node):
    def __init__(self, value):
        super().__init__(value=value)
    
    def __str__(self):
        return str(self.value)

    def operate(self):
        return {'1': self.value}

    def assign(self, dic):
        return Constant(self.value)



class Variable(Node):
    def __init__(self, name, value=None):
        super().__init__(name=name, value=value)

    def __str__(self):
        if self.value is None:
            return self.name
        return str(self.value)
        
    def operate(self):
        # TODO: var_names
        if self.value is None:
            return {self.name: 1}
        return self.value.operate()
        
    def collapse(self):
        if self.value is None:
            return Variable(self.name, self.value)
        return self.value.collapse

    def assign(self, dic):
        if self.name in dic.keys():
            item = dic[self.name]
            if isinstance(item, Node):
                return item 
            # else: may be a numeric literal
            return Constant(item)
        else:
            return self.value.assign(dic)



class Operator(Node):
    def __init__(self, children):
        children = [Constant(x) if not isinstance(x, Node) else x for x in children]
        super().__init__(children=children)



class Add(Operator):
    def __init__(self, x, y):
        super().__init__([x, y])
    
    def __str__(self):
        x, y = self.children
        return str(x) + ' + ' + str(y)

    def operate(self):
        # TODO: var_names
        x, y = map(lambda v: v.operate(), self.children)
        for name, value in y.items():
            if name in x:
                x[name] += value 
            else:
                x[name] = value
        return x

    def assign(self, dic):
        x, y = self.children
        return Add(x.assign(dic), y.assign(dic))
