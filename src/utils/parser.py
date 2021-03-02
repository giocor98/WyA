from variables import Variable, AskVariable, AlwaysAskVariable
from scope import Dir

def parseVar(var, name):
    if not isinstance(var, str):
        raise Excepion ("Need to parse a string!!")

    if "auto" == name:
        var = var.split(':')
        nome = var[0]
        var = var[1]

    if var.startWidth("?"):
        return AskVariable(name, var[1:])
    elif var.startWidth("!"):
        return AlwaysAskVariable(name, var[1:])
    elif var.startWidth("["):
        var = var[1:][:-1]
        var = var.split(',')
        ret = Dir(name)
        for l in var:
            ret.add(parseVar(l, "auto"))
        return ret
    elif var.startWidth('"'):
        return Variable(name, var[1:])
    else:
        return Variable(name, var)
