from lxml.html import html5parser
from postformat import Question
from icecream import ic
from postformat import Question
from imageProcessor import Converter

class HTMLParser:

    def __init__(self, fileName):
        self.fileName = fileName
        self.allLines = []
        self.__rawLines = []
        self.Questions = []
        self.assesmentName = ''
        self.Description = ''
        self.questionInstances = []
        # Parse through the lines unparsed
        self.__readRawLines()
        # Read through the lines as a string
        self.__parseFile()
        # Parse through each line and organize each question
        self.__parseLines()
        # Link the questions alongside images
        self.addImages()
        # Create an image and process it
        self.__writeImages()
    
    '''
    Creates a Converter class for eaach image
    '''
    def __writeImages(self):
        for question in self.questionInstances:
            if question.hasImage():
                Converter(question.getImageURL(),f'Image{self.questionInstances.index(question)+1}.jpg')

    '''
    Reads the file as unparsed text
    '''
    def __readRawLines(self):
        self.__rawLines = open(self.fileName,'r').readlines()

    # The next two methods are very, very janky

    '''
    Matches the unparsed lines with the parsed counterparts
    '''
    def __matchRawWithCooked(self):
        matched = []
        for parsedLines in self.allLines:
            for rawLines in self.__rawLines:
                if parsedLines in rawLines and 'src' in rawLines and not 'SERVER.GRAPHICS' in rawLines:
                    matched.append([parsedLines, rawLines])
        return matched
    

    '''
    Matches the unparsed lines with that of the question,
    allowing for the image to be saved
    '''
    def addImages(self):
        matched = self.__matchRawWithCooked()
        for parsed, raw in matched:
            for question in self.questionInstances:
                if parsed in question.getText():
                    base64Data = raw.split('base64,')[1].split('\" ')[0]
                    question.setImg(base64Data)

    '''
    Parses the text and only the text into a list of strings
    '''
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
                questionInstance = self.__questionDescription(line,questionInstance,outcomes)
                outcomes, onOutcomes = [], False
            elif 'Question ID:' in line:
                questionInstance.setID(line.split('Question ID: ')[1])
            elif 'Meta Tags:' in line:
                onMetaTags = True
            elif line in questionInstance.getText():
                continue
            elif 'Outcomes:' in line:
                onMetaTags, onOutcomes = False, True
            elif onOutcomes:
                if  len(outcomes) <= len(questionInstance.getAnswers()) and 'choice' in line:
                    outcomes.append(line)
            elif not onOutcomes and not onMetaTags:
                questionInstance = self.__parseAnswersAndTypes(line, questionInstance)

        self.__postLoop(questionInstance, outcomes)
    
    '''
    Method to parse the description of a question, as well as to reset any question instances
    Inputs:
        line (str): The current line that is being parsed
        questionInstance (Question): The current instance that data can be saved to
        outcomes ([str,...]): A list of all of the outcomes to be used by the Question instance
    '''
    def __questionDescription(self, line, questionInstance, outcomes):
        questionInstance.setRightAnswer(self.__calculateRightAnswer(questionInstance.getAnswers(),outcomes))
        self.questionInstances.append(questionInstance)
        del questionInstance
        question = line.split('Question Description: ')[1]
        if 'src=' in question:
            question, image = question.split('IMG' if 'IMG ' in question else 'img ')
        else:
            image = None
        return Question(TYPE='MC',text=question,img=image)

    '''
    Method to parse the answers, as well as find what type on question is being read
    Inputs:
        line (str): The current line that is being parsed
        questionInstance (Question): The current instance that data can be saved to
    '''
    def __parseAnswersAndTypes(self, line, questionInstance):
        answerStarts = ['(a)','(b)','(c)','(d)','(Q)']
        if not any(start in line for start in answerStarts) and not (line.startswith('(')):
            questionInstance.addAnswer(line)
            if line == 'True' or line == 'False':
                questionInstance.setType('TF')
        return questionInstance
    
    '''
    Method that contains all instructions on what is to be run at the end of the parsing loop
    Inputs:
        questionInstance (Question): The current question instance used to both set and recieve data from
        outcomes ([str,...]): A list of all of the outcomes to be used by the Question instance
    '''
    def __postLoop(self, questionInstance, outcomes):
        questionInstance.setRightAnswer(self.__calculateRightAnswer(questionInstance.getAnswers(),outcomes))
        self.questionInstances.append(questionInstance)
        # Remove the first empty question
        self.questionInstances.remove(self.questionInstances[0])
        ic(self.questionInstances)
        '''for question in self.questionInstances:
            ic(str(question))'''
        print(f'{len(self.questionInstances)} Questions found')

    def getQuestions(self):
        return self.questionInstances
    
    def __calculateRightAnswer(self, answers, outcomes):
        for outcome in outcomes:
                    if 'set score to 1' in outcome:
                        return answers[outcomes.index(outcome)]
                    