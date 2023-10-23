from parser import Parser
from writer import Writer
from postformat import Formatter

fileName = 'PCs DHJ to Sharon Hill Test.html'

p = Parser(fileName)
f = Formatter(p.getQuestions())
w = Writer(fileName, f.getDataTable())
