class Question:
    
    def __init__(self, TYPE : str, text : str, answers, rightAnswer : str, img : str = None):
        self.__TYPE = TYPE
        self.__text = text
        self.__answers = answers
        self.__rightAnswer = rightAnswer
        self.__rightAnswerIndex = self.__answers.index(self.__rightAnswer)
        self.__imageURL = img
        
    def getText(self):
        return self.__text
    
    def getAnswers(self):
        return self.__answers
        
    def getType(self):
        return self.__TYPE
    
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
    