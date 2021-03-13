from variables import Variable


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

    def getCmd(self):
        return self.cmd

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
