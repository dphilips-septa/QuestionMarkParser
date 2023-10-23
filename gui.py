from tkinter import LEFT, RIGHT, StringVar, TOP
from tkinterdnd2 import TkinterDnD, DND_ALL
import customtkinter as ctk
import os
from parser import Parser
from parsetest import HTMLParser
from writer import Writer
from postformat import Formatter

global fileName

# Create class to allow for customtkinter to take over rendering
class Tk(ctk.CTk, TkinterDnD.DnDWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.TkdndVersion = TkinterDnD._require(self)

ctk.set_appearance_mode("dark")

def get_path(event):
    global fileName
    forbiddenCharacters = ['{','}']
    data = event.data
    # Remove any characters that windows might insert
    for character in forbiddenCharacters:
        data = data.replace(character,'')
    fileName = data
    writeMessage(os.path.split(fileName)[-1])

def run():
    # Inform user that program is running
    writeMessage('Loading')

    # Create and begin file parser
    p = HTMLParser(fileName)

    # Create and begin output formatter
    f = Formatter(p.getQuestions())

    # Create and begin output writer
    w = Writer(fileName, f.getDataTable())

    # Inform users of completion
    writeMessage('Extraction and formatting completed')

def clear():
    writeMessage("Drag and drop file in the entry box")

def writeMessage(message):
    pathLabel.configure(text=message)

# Create and set paramaters for window
root = Tk()
root.geometry("350x100")
root.title("Jennis")


# Create the drag and drop entry box
entryWidget = ctk.CTkEntry(root)
entryWidget.pack(side=TOP, padx=5, pady=5)

# Create the text box to keep users up to date
pathLabel = ctk.CTkLabel(root, text="Drag and drop file in the entry box")
pathLabel.pack(side=TOP)

# Create the clear button in order to allow user to input new file
clearButton = ctk.CTkButton(root, text='Clear', command=clear)
clearButton.pack(side=LEFT)

# Create the run button in order to allow user to start program when desired
runButton = ctk.CTkButton(root, text='Run', command=run)
runButton.pack(side=RIGHT)

# Create drag and drop command
entryWidget.drop_target_register(DND_ALL)
entryWidget.dnd_bind("<<Drop>>", get_path)

root.mainloop()