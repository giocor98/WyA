from ./../../utils/scope import Scope, Dir
from ./../../utils/variables import Variable, AskVariable, AlwaysAskVariable
import ./../../utils/parser

class Cmd (Dir):

    def __init__(self, name, cmd, req, answ):
        super(name)
        self.add(parseVar(cmd, "cmd"))
        self.add(parseVar(req, "req"))
        self.add(parseVar(answ, "answ"))


    def
