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
