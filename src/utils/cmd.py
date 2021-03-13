from scope import Scope, Dir
from variables import Variable, AskVariable, AlwaysAskVariable
from parser import Parser

import subprocess
from time import sleep
from threading import Thread


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






s = Scope.getInstance()
s.addCmd(Cmd("cmd1", "echo ciao", "[ciao:$cmd4]", "[async:True]"))
s.addCmd(Cmd("cmd2", "echo goon", "[ciao:!what?!,goon:$cmd4]", "[async:True]"))
s.addCmd(Cmd("cmd3", "echo start", "[start:$cmd2]", "[async:True]"))
s.addCmd(Cmd("cmd4", "echo end", "[ciao:!what?!,end:!ended lol]", "[async:True]"))
s.tree()
s.getCmd().get("cmd1").exeCmd()
s.getCmd().get("cmd2").exeCmd()

print("LOL, finito")
