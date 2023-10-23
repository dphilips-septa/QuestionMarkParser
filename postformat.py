class Question:
    
    def __init__(self, TYPE : str = "", text : str = "", ID : str = "", answers : list = None, rightAnswer : str = "", img : str = None): # type: ignore
        self.__TYPE = TYPE
        self.__text = text
        self.__ID = ID
        self.__answers = [] if answers is None else answers
        self.__rightAnswer = rightAnswer
        self.__rightAnswerIndex = None
        try:
            self.__rightAnswerIndex = self.__answers.index(self.__rightAnswer)
        except:
            pass
        self.__imageURL = img
        self.__hasGivenRightAnswerError = False 
        self.__fixedError = False
    
    def setType(self, TYPE):
        self.__TYPE = TYPE
    
    def setText(self, text):
        self.__text = text

    def setID(self, ID):
        self.__ID = ID
    
    def addAnswer(self, answer):
        self.__answers.append(answer)
        try:
            if self.__hasGivenRightAnswerError and not self.__fixedError:
                self.setRightAnswer(self.__rightAnswer)
        except:
            pass

    
    def setRightAnswer(self, answer):
        self.__rightAnswer = answer
        try:
            self.__rightAnswerIndex = self.__answers.index(self.__rightAnswer)
            if self.__hasGivenRightAnswerError and not self.__fixedError:
                print('Error Fixed')
                self.__fixedError = True
        except:
            print("Warning, the right answer that you have provided is not an existing answer within this question, please make sure to add it to minimize the chance of errors")
            self.__hasGivenRightAnswerError = True
    def setImg(self, img):
        self.__imageURL = img
        
    def getText(self):
        return self.__text
    
    def getAnswers(self):
        return self.__answers
        
    def getType(self):
        return self.__TYPE
    
    def getID(self):
        return self.__ID

    def getRightAnswer(self):
        return self.__rightAnswer
    
    def getRightAnswerIndex(self):
        return self.__rightAnswerIndex
    
    def hasImage(self):
        return self.__imageURL != None

    def getImageURL(self):
        return self.__imageURL

    def __str__(self):
        noImage = f'text: {self.__text}\nanswers: {self.__answers}\nright answer:{self.__rightAnswer}'
        if self.__imageURL is not None:
            noImage += '\nImage: Has Image'
        return noImage
    
    def __len__(self):
        return len(self.__answers)

class Formatter:
    
    def __init__(self, questions):
        self.questions = questions
        self.__dataTable = None
        self.__format()

    # Create the data array used to store all questions and answers
    # Last edit by Daniel Philips, 10/16/2023
    def __format(self):
        maxNumQuestions = len(max(self.questions, key=len))

        # Add the header line to the data array
        self.__dataTable = [ ["//Question Text", "//Question Text"] + [f'//Answer Choice {f}' for f in range(1, maxNumQuestions + 1)] ]
        
        for question in self.questions:
            self.__dataTable.append(self.__formatLine(question))
    
    # Formats a given line based on the importing template
    # Last edit by Daniel Philips, 10/17/2023
    def __formatLine(self, line):
        # Format a given line into the required format for Storyline
        toReturn = [line.getType(), line.getText()] + [answer for answer in line.getAnswers()]

        # Indicate which answer is the right answer using an asterix
        toReturn[line.getRightAnswerIndex() + 2] = '*' + toReturn[line.getRightAnswerIndex() + 2]
        return toReturn
    
    def getDataTable(self):
        return self.__dataTable
    