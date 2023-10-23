from postformat import Question
from imageProcessor import Converter
class Parser:

    def __init__(self, fileName):
        self.fileName = fileName
        self.__questions, self.startEnds = [], []
        self.__readFile()
        self.__spliter()
        self.__perQuestion()

    def __readFile(self):
        file = open(self.fileName,'r')
        self.__allData = file.readlines()
    
    # Parses each line, finding the lines that each question starts and ends on
    # Last edit by Daniel Philips, 10/16/2023
    def __spliter(self):
        start = -1
        for part in self.__allData:
            # Detect the start of a new question
            if 'qm_NUMBER' in part:
                if start != -1:
                    prevStart = start
                    prevEnd = self.__allData.index(part) - 2
                    self.startEnds.append( [prevStart, prevEnd] ) 
                    print([prevStart,prevEnd])
                start = self.__allData.index(part)

    # Parses all lines and extracts data pertaining to each question
    # Last edit by Daniel Philips, 10/16/2023
    def __perQuestion(self):
        for questionBoundary in self.startEnds:
            # Set defaults for each question
            questionType, answers = 'MC', []
            question, rightAnswer = '', ''
            currentNumFeedback, numFeedback = 0, 0
            image = None
            
            # Save all lines for the given question
            allLinesForQuestion = self.__allData[questionBoundary[0] : questionBoundary[1]]
            
            for line in allLinesForQuestion:

                # Detect the question type, mc (Multiple Choice) or tf (True or False)
                if'qm_CHOICE_tf' in line:
                    questionType = 'TF'
                
                # Check if you are reading the answer choices
                # If the choice for A is being read and the answer is wrong, read the right answer
                if 'if choice' in line.lower() and 'is selected' in line.lower():
                    if 'wrong' not in line.lower():
                        numFeedabck = currentNumFeedback
                    else:
                        currentNumFeedback += 1

                # Detect whether this line is displaying visible text
                elif 'qm_HTML_CONTENT' in line:
                    data = self.__extractText(line)
                    # If the line contains an answer choice, save it to answers[]
                    if 'qm_CHOICE_' in line:
                        answers.append(data)
                    
                    # If the line contains question content, save the text to the variable question
                    elif 'qm_QA_CONTENT' in line:
                        if '<img' in line.lower():
                            isCaps = True if '<IMG' in line else False
                            question = data.split('<IMG')[0] if isCaps else data.split('<img')[0]
                            image = data.split('base64,')[1].split('\" width=')[0]
                            if len(data.split('src=\"')) > 2:
                                print('\n\tMore than one image found!\n\tOnly the first image has been saved')
                        else:
                            question = data
                            
            rightAnswer = answers[numFeedabck]

            # Create question instance using parsed values
            questionInstance = Question(questionType, question, answers, rightAnswer, image)
            self.__questions.append(questionInstance)

            print(questionInstance)
            print(' ')
        self.__saveImages()

    # Extracts text from the HTML removing requriment for external libraries
    # Arguments:
    #   line: A string line containing a line of HTML code
    # Last edit by Daniel Philips, 10/16/2023
    def __extractText(self, line):
        return line.split('<div>')[1].split('</div>')[0].replace('&nbsp;','')
    
    def getQuestions(self):
        return self.__questions
    
    def __saveImages(self):
        for i in range(len(self.__questions)):
            question = self.__questions[i]
            if question.hasImage():
                url = question.getImageURL()
                converter = Converter(url,f'ImageFor{i+1}.jpg')

    