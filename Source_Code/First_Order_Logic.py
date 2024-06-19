import random

from nltk.sem import Expression
from nltk.inference import ResolutionProver
import pandas

class FOL:
    def __init__(self):
        self.data = pandas.read_csv('Knowledge_Base.csv', header=None)
        self.kb = []
        self.rs = ResolutionProver()
        self.loadKB()

    def loadKB(self):
        for row in self.data[0]:
            expr = Expression.fromstring(row)
            self.kb.append(expr)

    def contradicts(self,expr):
        if ResolutionProver().prove(expr.negate(), self.kb, verbose=False):
            return True
        else:
            return False

    def processInput(self,userInput):
        object = userInput[1].split(' IS ')[0].lower()
        subject = userInput[1].split(' IS ')[1].lower()
        expr = Expression.fromstring(subject + '(' + object + ')')
        return object,subject,expr

    def prove(self, userInput):
        object,subject,expr = self.processInput(userInput)
        answerPositive = ResolutionProver().prove(expr, self.kb, verbose=False)
        answerNegative = ResolutionProver().prove(expr.negate(), self.kb, verbose=False)
        return answerPositive, answerNegative

    def proveFalse(self, userInput):
        object,subject,expr = self.processFalseInput(userInput)
        answerPositive = ResolutionProver().prove(expr, self.kb, verbose=False)
        answerNegative = ResolutionProver().prove(expr.negate(), self.kb, verbose=False)
        return answerPositive, answerNegative

    def addNewStatement(self, userInput):
        object, subject, expr = self.processInput(userInput)
        if not self.contradicts(expr):
            self.kb.append(expr)
            return True
        else:
            return False

    def getQuestion(self):
        breeds = []
        for each in self.kb:
            each = str(each)
            each = each.replace(")", "")
            eachsplit = each.split("(")
            if eachsplit[0] == "dog" or eachsplit[0] == "cat":
                breeds.append(eachsplit)
        return random.choice(breeds)

    def addNewFalseStatement(self, userInput):
        object, subject, expr = self.processFalseInput(userInput)
        if not self.contradicts(expr.negate()):
            self.kb.append(expr.negate())
            return True
        else:
            return False

    def processFalseInput(self, userInput):
        object = userInput[1].split(' IS NOT ')[0].lower()
        subject = userInput[1].split(' IS NOT ')[1].lower()
        expr = Expression.fromstring(subject + '(' + object + ')')
        return object, subject, expr

