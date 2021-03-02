from scope import Scope
from variables import Variable, AskVariable, AlwaysAskVariable


def proofFun(v2):
    print(v2)
    print("DONE")
    print(v2.getValue())
    print("Found:")
    print(v2.getValue())
    try:
        v2.unValidate()
    except:
        print("none")
    print(v2.getValue())


v1 = Variable("obj1", "test1")
v2 = AskVariable("obj2", "test2:")
v3 = AlwaysAskVariable("obj3", "Che ci metto?")
v4 = Variable("oo", "t2")

proofFun(v1)
proofFun(v2)
proofFun(v3)
proofFun(v4)
proofFun(v1)

s = Scope.getInstance()
print(s)
s.print()
s.add(v1)
s.print()
s.mkdir("home")
s.print()
s.cd("home")
s.print()
s.add(v2)
s.print()
s.add(v3)
s.print()
s.tree()
