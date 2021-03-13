import subprocess
from time import sleep
from threading import Thread


class Variable:

    __name = ""
    __value = ""

    ## Constructor
    def __init__ (self, name, stringa):
        self.__name = name
        self.__value = stringa

    def getName(self):
        return self.__name

    def getValue(self):
        return self.__value

    def setValue(self, value):
        self.__value = value

class AskVariable(Variable):

    __question = ""
    __setted = False

    ## Constructor
    def __init__ (self, name, question):
        super().__init__(name, "")
        self.__question = question

    def getValue(self):
        if not self.__setted :
            super().setValue( input(self.__question))
            self.__setted = True
        return super().getValue()

    def unValidate(self):
        self.__setted = False

class AlwaysAskVariable(Variable):

    ## Constructor
    def __init__ (self, name, question):
        super().__init__(name, question)

    def getValue(self):
        return input(super().getValue())


class DelayedCmd(Variable):

    def __init__ (self, name, stringa):
        Variable.__init__(self, name, stringa)

    def getValue(self):
        try:
            Scope.getInstance().getCmd().get(Variable.getValue(self)).exeCmd()
            return ""
        except Exception as e:
            print (e)
            print("Deferred load had an excception")
            return ""

class DelayedVar(Variable):

    def __init__ (self, name, stringa):
        Variable.__init__(self, name, stringa)

    def getValue(self):
        try:
            return Scope.getInstance().getVar().get(Variable.getValue(self)).getValue()
        except Exception as e:
            print (e)
            print("Deferred load had an excception")
            return ""


class Dir:

    __variables = {}
    __subDirs = {}
    __name = ""


    def __init__(self, name):
        self.__name = name
        self.__subDirs = {}
        self.__variables = {}

    def getName(self):
        return self.__name


    def __setVar(self, var, name):
        if self.__canBeAdded(name):
            self.__variables[name] = var

    def __rmVar(self, name):
        del self.__variables[name]

    def getVar(self, name):
        return self.__variables[name]

    def __setDir(self, dir, name):
        if self.__canBeAdded(name):
            self.__subDirs[name] = dir

    def __rmDir(self, dir, name):
        del self.__subDirs[name]

    def getDir(self, name):
        return self.__subDirs[name]


    def __canBeAdded(self, name):
        return not name in (list(self.__variables.keys()) + list(self.__subDirs.keys()))

    def __isInDir(self, name):
        return name in list(self.__subDirs.keys())

    def __isInVar(self, name):
        return name in self.__variables.keys()

    def __isDir(dir):
        return isinstance(dir, Dir)

    def __isVar(var):
        return isinstance(var, Variable)


    def createDir(self, dir):
        if (Dir.__isDir(dir)):
            try:
                self.__setDir(dir, dir.getName())
                return True
            except:
                return False
        else:
            return False

    def createVar(self, var):
        if (self.__canBeAdded(var.getName()) and Dir.__isVar(var)):
            try:
                self.__setVar(var, var.getName())
                return True
            except:
                return False
        else:
            return False


    def removeDir(self, name):
        if name in self.__subDirs.keys():
            try:
                self.__rmDir(name)
                return True
            except:
                return False
        else:
            return True

    def removeVar(self, name):
        if name in self.__variables.keys():
            try:
                self.__rmVar(name)
                return True
            except:
                return False
        else:
            return True



    def get(self, x):
        if not isinstance(x, str):
            name = x.getName()
        else:
            name = x
        try:
            if self.__isInDir(name):
                return self.getDir(name)
            elif self.__isInVar(name):
                return self.getVar(name)
            else:
                raise Exception("not found: " + name + " in: " + self.getName())
        except Exception as e:
            raise Exception("Unexpected error:\n" + str(e))


    def add(self, x):
        if not self.createDir(x):
            if not self.createVar(x):
                return False
        return True


    def rm(self, x):
        if not self.removeDir(x):
            if not self.removeVar(x):
                return False
        return True


    def __print(self, pre):
        for el in self.__variables.keys():
            print(pre + " " + el)
        for d in self.__subDirs.keys():
            if d == self.getName():
                print(pre + "X")
            else:
                print(pre + " -" + d + ":")
                (self.__subDirs[d]).__print(pre+"|")


    def print(self):
        self.__print("|")


class Scope:

    __dirs = []
    __instance= None

    @staticmethod
    def getInstance():
        if Scope.__instance == None:
            Scope()
        return Scope.__instance

    def __init__(self):
        if Scope.__instance != None:
            raise Exception ("ERROR: The Sccope is a singleton!!")
        else:
            Scope.__instance = self
        self.push(Dir(""))
        self.cmd = self.mkdir("cmd")
        self.var = self.mkdir("var")

    def getCmd(self):
        return self.cmd

    def getVar(self):
        return self.var

    def __isDir(dir):
        return isinstance(dir, Dir)

    def getLast(self):
        return self.__dirs[-1]

    def push(self, dir):
        if isinstance(dir, Dir):
            self.__dirs.append(dir)
            return True
        else:
            return False

    def pop(self):
        self.__dirs.pop()

    def get(self, name):
        for d in self.__dirs[::-1]:
            try:
                return d.get(name)
            except:
                pass
        raise Exception ("Directory not found: "+ name)

    def mkdir(self, name):
        d = Dir(name)
        self.getLast().add(d)
        return d


    def add(self, x):
        return self.getLast().add(x)

    def addCmd(self, x):
        return self.getCmd().add(x)

    def addVar(self, x):
        return self.getVar().add(x)


    def rm(self, x):
        return self.getLast().rm(x)

    def cd(self, name):
        if name == "..":
            self.pop()
        else:
            self.push(self.get(name))



    def print(self):
        print("print")
        self.getLast().print()

    def tree(self):
        print("tree")
        self.__dirs[0].print()


class Parser:

    def parseLine(stringa):
        if stringa.startswith("cmd "):
            stringa = stringa[4:]
            nome = stringa.split("=")[0].strip()
            val = stringa.split("=")[1].split(";")
            val[0] = val[0].strip()
            val[1] = val[1].strip()
            val[2] = val[2].strip()
            Scope.getInstance().addCmd(Cmd(nome, val[0], val[1], val[2]))
        elif stringa.startswith("var "):
            stringa = stringa[4:]
            nome = stringa.split("=")[0].strip()
            val = stringa.split("=")[1].strip()
            Scope.getInstance().addVar(Parser.parseVar(val, nome))


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
        elif var.startswith("$cmd/"):
            var = var[5:]
            return DelayedCmd(name, var)
        elif var.startswith("$var/"):
            var = var[5:]
            return DelayedVar(name, var)
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


class Cmd (Dir, Thread):

    def __init__(self, name, cmd, req, param):
        Dir.__init__(self, name)
        Thread.__init__(self)
        self.add(Parser.parseVar(cmd, "cmd"))
        self.add(Parser.parseVar(req, "req"))
        self.add(Parser.parseVar(param, "param"))
        self.__running = False
        self.__goOn = True
        Thread.setName(self, name)

    def isRunning(self):
        return self.__running

    def __parseCmd(self):
        return self.get("cmd").getValue().split(' ')

    def getCheckNum(self):
        try:
            return int(self.get("param").get("checkNum").getValue())
        except:
            return 5 #default value

    def getTimeOut(self):
        try:
            return int(self.get("param").get("timeOut").getValue())
        except:
            return 1 #default value

    def getAsync(self):
        try:
            return "True" == self.get("param").get("async").getValue()
        except:
            return False #default value

    def readIn(self):
        if not self.isRunning():
            raise Exception("not started")
        l = self.proc.stdout.readline().decode("utf-8")
        ret = ""
        init="cmd." + self.getName() + ">"
        while l!= "":
            print(init + l)
            ret = ret + l
            l = self.proc.stdout.readline().decode("utf-8")
        return ret

    def writeOut(self, wr):
        if not self.isRunning():
            raise Exception("not started")
        init="cmd." + self.getName() + "<"
        print(init + wr)
        if not wr.endswith("\n"):
            wr = wr + "\n"
        self.proc.stdout.write(wr)
        return ret

    def checkAnswer(self, req):
        return self.get("req").get(req).getValue()

    def readAndWrite(self):
        i = self.readIn()
        for l in i.splitlines():
            l = l.strip()
            try:
                t = self.checkAnswer(l)
                if t == "quit()":
                    return False
                self.writeOut(t)
            except Exception as e:
                pass

        return True

    def run(self):
        if self.isRunning():
            raise Exception("Already running")
        n = self.getCheckNum()
        self.__running = True
        try:
            self.proc = subprocess.Popen(self.__parseCmd(),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            if(n==-1):
                while self.__goOn:
                    sleep(self.getTimeOut())
                    if not self.readAndWrite():
                        self.quit()
            else:
                for i in range(n):
                    if not self.__goOn:
                        break
                    sleep(self.getTimeOut())
                    self.readAndWrite()

        except Exception as e:
            raise e
        finally:
            self.__running = False


    def exeCmd(self):
        if self.isRunning():
            raise Exception("Already running")
        self.start()

    def quit(self):
        self.proc.kill()
        self.__goOn = False

Parser.parseLine("cmd cmd1 = echo ciao; [ciao:$var/aaVar]; [async:True]")
Parser.parseLine("cmd cmd2 = echo ciao; [ciao:$var/aaVar]; [async:True]")
Parser.parseLine("cmd cmd3 = echo ciao; [ciao:$var/aVar]; [async:True]")
Parser.parseLine("cmd cmd4 = echo ciao; [ciao:$var/aVar]; [async:True]")
Parser.parseLine("var aaVar = ?Always:")
Parser.parseLine("var aVar = !Once:")
s = Scope.getInstance()
s.tree()
s.getCmd().get("cmd1").exeCmd()
s.getCmd().get("cmd2").exeCmd()
s.getCmd().get("cmd3").exeCmd()
s.getCmd().get("cmd4").exeCmd()

print("LOL, finito")
