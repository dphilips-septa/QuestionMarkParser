from re import T
from lxml.html import html5parser
from postformat import Question

class Parser:

    def __init__(self, fileName):
        self.__fileName = fileName
        self.__readFile()
        self.QuestionInstances = []
        self.__splitter()

    def __readFile(self):
        file = open(self.__fileName,'r')
        unformattedLines = file.read()
        dataWithEmptyLines = html5parser.fromstring(unformattedLines).xpath("string()").split('\n')
        for i in range(len( dataWithEmptyLines ) - 1, 0, -1):
            #print(f'Index: {i}, Length: {len(dataWithEmptyLines)}')
            line = self.__formatLine(dataWithEmptyLines[i])
            if line != -1:
                dataWithEmptyLines[i] = line.replace('\xa0','')
            else:
                dataWithEmptyLines.remove(dataWithEmptyLines[i])
        self.__allData = dataWithEmptyLines


    def __formatLine(self, line):
        return -1 if line.isspace() or line == '' else line.strip()

    def __splitter(self):
        clearQuestionInformation = {
            'Type' : '',
            'Question' : '',
            'ID' : '',
            'Answers' : [],
            'Right Answer' : '',
            'Outcomes' : [],
            'Image' : None
        }
        questionInformation = clearQuestionInformation
        onOutcomes = False
        onMetaTags = False
        
        for line in self.__allData:
            if 'Question Description:' in line:
                if questionInformation['ID'] != '':
                    print(questionInformation)
                    q = Question('MC',questionInformation['Question'],questionInformation['Answers'],
                                 questionInformation['Right Answer'], questionInformation['Image'])
                    print(q)
                    self.QuestionInstances.append(q)
                    questionInformation = clearQuestionInformation
                    onOutcomes = False
                    onMetaTags = False
                question = line.split('Question Description: ')[1]

                if 'scr=' in question:
                    toSplit = 'IMG' if 'IMG ' in question else 'img '
                    question, image = question.split(toSplit)
                else:
                    image = None
                questionInformation['Image'] = image
                questionInformation['Question'] = question
            elif 'Question ID: ' in line:
                onMetaTags = False
                questionInformation['ID'] = line.split('Question ID: ')[1]
            elif 'Meta Tags:' in line:
                onMetaTags = True
            elif line in questionInformation['Question']:
                continue
            elif 'Outcomes:' in line:
                onOutcomes = True
            elif onOutcomes:
                if len(questionInformation['Outcomes']) <= len(questionInformation['Answers']):
                    questionInformation['Outcomes'].append(line)
            elif not onOutcomes and not onMetaTags:
                answerStarts = ['(a)','(b)','(c)','(d)']
                if not any(start in line for start in answerStarts):
                    questionInformation['Answers'].append(line)




p = Parser("PCs DHJ to Sharon Hill Test.html")