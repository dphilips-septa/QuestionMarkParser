from lxml.html import html5parser
from postformat import Question
from icecream import ic
from postformat import Question

class HTMLParser:

    def __init__(self, fileName):
        self.fileName = fileName
        self.allLines = []
        self.Questions = []
        self.assesmentName = ''
        self.Description = ''
        self.questionInstances = []
        self.__parseFile()
        self.__parseLines()
    
    def __parseFile(self):
        lines = open(self.fileName,'r').read()
        doc = html5parser.fromstring(lines)
        self.allLines = doc.xpath("string()").split('\n')
        for i in range(len(self.allLines)-1, -1, -1):
            formatted = self.__formatLine(self.allLines[i])
            if formatted != -1:
                self.allLines[i] = formatted
            else:
                self.allLines.remove(self.allLines[i])

    def __formatLine(self, line):
        if line.isspace() or line == '':
            return -1
        else:
            return line.strip()



    
    
    def __parseLines(self):
        onOutcomes = False
        onMetaTags = False
        outcomes = []
        questionInstance = Question()
        for line in self.allLines:
            if 'created by wizard' in line or 'ofÂ' in line:
                continue
            line = line.replace('\xa0','')
            if 'Question Description:' in line:

                # Parse right answer
                questionInstance.setRightAnswer(self.__calculateRightAnswer(questionInstance.getAnswers(),outcomes))
                outcomes = []
                onOutcomes = False
                self.questionInstances.append(questionInstance)
                del questionInstance
                question = line.split('Question Description: ')[1]

                if 'src=' in question:
                    toSplit = 'IMG' if 'IMG ' in question else 'img '
                    question, image = question.split(toSplit)
                else:
                    image = None
   
                questionInstance = Question(TYPE='MC',text=question,img=image)
            elif 'Question ID:' in line:
                questionInstance.setID(line.split('Question ID: ')[1])
            elif 'Meta Tags:' in line:
                onMetaTags = True
            elif line in questionInstance.getText():
                continue
            elif 'Outcomes:' in line:
                onMetaTags = False
                onOutcomes = True
            elif onOutcomes:
                if len(outcomes) <= len(questionInstance.getAnswers()) and 'choice' in line:
                    outcomes.append(line)
            elif not onOutcomes and not onMetaTags:
                answerStarts = ['(a)','(b)','(c)','(d)','(Q)']
                if not any(start in line for start in answerStarts) and not (line.startswith('(')):
                    questionInstance.addAnswer(line)
                    if line == 'True' or line == 'False':
                        questionInstance.setType('TF')


        questionInstance.setRightAnswer(self.__calculateRightAnswer(questionInstance.getAnswers(),outcomes))
        self.questionInstances.append(questionInstance)
        # Remove the first empty question
        self.questionInstances.remove(self.questionInstances[0])
        print(f'{len(self.questionInstances)} Questions found')
    
    def getQuestions(self):
        return self.questionInstances
    
    def __calculateRightAnswer(self, answers, outcomes):
        for outcome in outcomes:
                    if 'set score to 1' in outcome:
                        return answers[outcomes.index(outcome)]