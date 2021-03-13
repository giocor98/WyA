from variables import Variable, AskVariable, AlwaysAskVariable, DelayedCmd
from scope import Dir, Scope

class Parser:


    def parseVar(var, name):
        if not isinstance(var, str):
            raise Excepion ("Need to parse a string!!")

        if "auto" == name:
            var = var.split(':')
            name = var[0]
            var = var[1]

        if var.startswith("?"):
            return AskVariable(name, var[1:])
        elif var.startswith("!"):
            return AlwaysAskVariable(name, var[1:])
        elif var.startswith("$"):
            var = var[1:]
            return DelayedCmd(name, var)
        elif var.startswith("["):
            var = var[1:][:-1]
            var = var.split(',')
            ret = Dir(name)
            for l in var:
                ret.add(Parser.parseVar(l, "auto"))
            return ret
        elif var.startswith('"'):
            return Variable(name, var[1:])
        else:
            return Variable(name, var)
