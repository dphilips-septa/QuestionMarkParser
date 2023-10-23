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
        self.__parseFile()
        self.__parseLines()
        self.questionInstances = []
        self.__createQuestionInstances()
    
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
        questionData = {
            'Type' : 'MC',
            'Question' : '',
            'ID' : '',
            'Answers' : [],
            'Right Answer' : '',
            'Outcomes' : [],
            'Image' : None
        }

        onOutcomes = False
        onMetaTags = False
    
        for line in self.allLines:
            if 'created by wizard' in line or 'ofÂ' in line:
                continue
            line = line.replace('\xa0','')
            if 'Question Description:' in line:

                # Parse right answer
                outcomes = questionData['Outcomes']
                for outcome in outcomes:
                    if 'set score to 1' in outcome:
                        questionData['Right Answer'] = questionData['Answers'][questionData['Outcomes'].index(outcome)]

                self.Questions.append(questionData)
                onOutcomes = False

                question = line.split('Question Description: ')[1]

                if 'src=' in question:
                    toSplit = 'IMG' if 'IMG ' in question else 'img '
                    question, image = question.split(toSplit)
                else:
                    image = None


                questionData = {
                    'Type' : 'MC',
                    'Question' : question,
                    'ID' : '',
                    'Answers' : [],
                    'Right Answer' : '',
                    'Outcomes' : [],
                    'Image' : image
                }
            elif 'Question ID:' in line:
                questionData['ID'] = line.split('Question ID: ')[1]
            elif 'Meta Tags:' in line:
                onMetaTags = True
            elif line in questionData['Question']:
                continue
            elif 'Outcomes:' in line:
                onMetaTags = False
                onOutcomes = True
            elif onOutcomes:
                if len(questionData['Outcomes']) <= len(questionData['Answers']) and 'choice' in line:
                    questionData['Outcomes'].append(line)
            elif not onOutcomes and not onMetaTags:
                answerStarts = ['(a)','(b)','(c)','(d)','(Q)']
                if not any(start in line for start in answerStarts) and not (line.startswith('(')):
                    questionData['Answers'].append(line)
                    if line == 'True' or line == 'False':
                        questionData['Type'] = 'TF'

        # Remove the first empty question
        self.Questions.remove(self.Questions[0])

    def __createQuestionInstances(self):
        for question in self.Questions:
            self.questionInstances.append(
                Question(question['Type'],question['Question'],question['Answers'],question['Right Answer'],question['Image'])
            )
        print(f'{len(self.questionInstances)+1} Questions Found')
    
    def getQuestions(self):
        return self.questionInstances